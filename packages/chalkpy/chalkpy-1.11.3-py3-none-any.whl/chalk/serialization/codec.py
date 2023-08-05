from __future__ import annotations

import collections.abc
import dataclasses
import enum
from datetime import date, datetime, timezone
from typing import TYPE_CHECKING, Any, List, Type, Union, cast, get_origin, get_type_hints

import cattrs
import pendulum
import polars as pl
import pydantic
import pytz
from dateutil import parser
from pendulum.tz.timezone import Timezone
from polars.internals.construction import is_namedtuple
from typing_extensions import get_args

from chalk.serialization.parsed_annotation import ParsedAnnotation
from chalk.streams import Windowed
from chalk.utils.enum import get_enum_value_type
from chalk.utils.log_with_context import get_logger

if TYPE_CHECKING:
    from chalk.features import Feature

try:
    import attrs
except ImportError:
    # Imports not available. Attrs is not required.
    attrs = None

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import numpy as np
except ImportError:
    np = None

_log = get_logger(__name__)

_NoneType = type(None)


def _unwrap_optional_if_needed(typ: Type):
    if get_origin(typ) == Union and len(get_args(typ)) == 2:
        has_none = any(d == _NoneType for d in get_args(typ))
        if has_none:
            return next((m for m in get_args(typ) if m != _NoneType), None)

    return typ


def is_numeric(dtype: Union[pl.DataType, Type[pl.DataType]]) -> bool:
    return dtype in (
        pl.Float32,
        pl.Float64,
        pl.Int16,
        pl.Int8,
        pl.Int32,
        pl.Int64,
        pl.UInt8,
        pl.UInt16,
        pl.UInt32,
        pl.UInt64,
    )


class FeatureCodec:
    def __init__(self):
        self.converter = cattrs.Converter()
        self.converter.register_structure_hook(datetime, lambda v, _: parser.isoparse(v))
        self.converter.register_unstructure_hook(
            datetime,
            lambda v: (
                cast(datetime, v) if cast(datetime, v).tzinfo else pytz.utc.localize(cast(datetime, v))
            ).isoformat(),
        )

    def _default_encode(self, value: Any):
        if isinstance(value, set):
            return {self._default_encode(x) for x in value}
        if isinstance(value, list):
            return [self._default_encode(x) for x in value]
        if isinstance(value, (str, int, float)):
            return value
        if isinstance(value, enum.Enum):
            return self._default_encode(value.value)
        if isinstance(value, datetime):
            tz = value.tzinfo or (datetime.now(timezone.utc).astimezone().tzinfo)
            assert tz is not None
            return pendulum.instance(value, cast(Timezone, tz)).isoformat()
        if isinstance(value, date):
            return value.isoformat()
        if np is not None and isinstance(value, np.integer):
            return int(value)
        if np is not None and isinstance(value, np.floating):
            return float(value)
        if pd is not None and isinstance(value, pd.Timestamp):
            return pendulum.instance(value.to_pydatetime()).isoformat()
        if isinstance(value, pydantic.BaseModel):
            return value.dict()
        if (attrs is not None and attrs.has(type(value))) or dataclasses.is_dataclass(value):
            return self.converter.unstructure(value)
        if isinstance(value, collections.abc.Iterable):
            return [self._default_encode(x) for x in value]
        raise TypeError(f"Unable to encode value of type {type(value).__name__}")

    def encode(
        self,
        feature: Feature,
        value: Any,
    ):
        if value is None:
            return None

        if feature.encoder is not None:
            return feature.encoder(value)

        return self._default_encode(value)

    def encode_fqn(self, fqn: str, value: Any):
        from chalk.features import Feature

        return self.encode(Feature.from_root_fqn(fqn), value)

    def _default_decode_value(
        self,
        feature: Feature,
        value: Any,
    ):
        assert feature.typ is not None
        if issubclass(feature.typ.underlying, enum.Enum):
            value = feature.typ.underlying(value)
        if issubclass(feature.typ.underlying, datetime):
            value = parser.isoparse(value)
        elif issubclass(feature.typ.underlying, date):
            # note: datetime is a subclass of date, so we must be careful to decode accordingly
            value = date.fromisoformat(value)
        if issubclass(feature.typ.underlying, pydantic.BaseModel):
            return feature.typ.underlying(**value)
        elif (attrs is not None and attrs.has(feature.typ.underlying)) or dataclasses.is_dataclass(
            feature.typ.underlying
        ):
            return self.converter.structure(value, feature.typ.underlying)
        if not isinstance(value, feature.typ.underlying):
            raise TypeError(
                f"Unable to decode value {value} to type {feature.typ.underlying.__name__} for '{feature.root_fqn}'"
            )
        return value

    def _default_decode(
        self,
        feature: Feature,
        value: Any,
    ):
        assert feature.typ is not None
        if value is None:
            if feature.typ.is_nullable:
                return None
            else:
                raise ValueError(f"Value is none but feature {feature} is not nullable")
        if feature.typ.collection_type is not None and get_origin(feature.typ.collection_type) == set:
            if not isinstance(value, set):
                raise TypeError(f"Feature {feature} is a set but value {value} is not")
            return {self._default_decode_value(feature, x) for x in value}
        elif feature.typ.collection_type is not None and get_origin(feature.typ.collection_type) == list:
            if not isinstance(value, list):
                raise TypeError(f"Feature {feature} is a list but value {value} is not")
            return [self._default_decode_value(feature, x) for x in value]
        else:
            return self._default_decode_value(feature, value)

    def decode(
        self,
        feature: Feature,
        value: Any,
    ):
        if value is None:
            return None

        if feature.decoder is not None:
            return feature.decoder(value)

        return self._default_decode(feature, value)

    def decode_fqn(
        self,
        fqn: str,
        value: Any,
    ):
        from chalk.features import Feature

        return self.decode(Feature.from_root_fqn(fqn), value)

    def get_pandas_dtype(self, fqn: str) -> str:
        from chalk.features import Feature

        feature = Feature.from_root_fqn(fqn)
        typ = feature.typ
        assert typ is not None, "typ should be specified"
        underlying = typ.underlying
        if issubclass(underlying, enum.Enum):
            # For enums, require all members to have the same type
            underlying = get_enum_value_type(underlying)
        # See https://pandas.pydata.org/docs/user_guide/basics.html#basics-dtypes
        if issubclass(underlying, str):
            return "string"
        if issubclass(underlying, bool):
            return "boolean"
        if issubclass(underlying, int):
            return "Int64"
        if issubclass(underlying, float):
            return "Float64"
        if issubclass(underlying, datetime):
            # This assumes timezone-aware. For timezone-unaware the `pandas_dtype` must be set directly on the Feature
            return "datetime64[ns, utc]"
        _log.info(
            f"Defaulting to pandas type 'object' for fqn {fqn} of type {typ.underlying.__name__}. Set the `pandas_dtype` attribute for better specificity."
        )
        return "object"

    def get_polars_dtype(self, fqn: str) -> Union[pl.DataType, Type[pl.DataType]]:
        from chalk.features import Feature

        feature = Feature.from_root_fqn(fqn)
        if feature.polars_dtype is not None:
            return feature.polars_dtype
        typ = feature.typ
        assert typ is not None, "typ should be specified"
        underlying = typ.underlying
        dtype = self._get_pl_dtype_for_type(underlying, fqn)
        if typ.collection_type is not None:
            dtype = pl.List(dtype)
        return dtype

    def _get_pl_dtype_for_type(self, underlying: type | Windowed, fqn: str) -> Union[pl.DataType, Type[pl.DataType]]:
        # Polars seems to allow optional for any dtype, so we ignore it when computing dtypes
        underlying = _unwrap_optional_if_needed(underlying)
        if isinstance(underlying, Windowed):
            # If the parent window feature appears in a dataframe, then it's likely in a streaming resolver
            # Use the underlying type for that windowed feature
            return self._get_pl_dtype_for_type(underlying._kind, fqn)
        if issubclass(underlying, enum.Enum):
            # For enums, require all members to have the same type
            underlying = get_enum_value_type(underlying)
        if issubclass(underlying, str):
            return pl.Utf8
        if issubclass(underlying, bool):
            return pl.Boolean
        if issubclass(underlying, int):
            return pl.Int64
        if issubclass(underlying, float):
            return pl.Float64
        if issubclass(underlying, datetime):
            return pl.Datetime(time_unit="us", time_zone="UTC")
        if issubclass(underlying, date):
            return pl.Date
        if dataclasses.is_dataclass(underlying) or is_namedtuple(underlying, annotated=True):
            # Polars always treats dataclasses and namedtuples as structs
            annotations = get_type_hints(underlying)
            fields: List[pl.Field] = []
            for field_name, type_annotation in annotations.items():
                parsed_annotation = ParsedAnnotation(underlying=type_annotation)
                if not parsed_annotation.is_scalar:
                    raise TypeError(f"{fqn} cannot be another Features class ")
                underlying_dtype = self._get_pl_dtype_for_type(parsed_annotation.underlying, f"{fqn}.{field_name}")
                if parsed_annotation.collection_type is None:
                    fields.append(
                        pl.Field(
                            name=field_name,
                            dtype=underlying_dtype,
                        )
                    )
                else:
                    fields.append(pl.Field(name=field_name, dtype=pl.List(underlying_dtype)))
            return pl.Struct(fields=fields)
        _log.info(
            f"Defaulting to polars type 'object' for fqn {fqn} of type {underlying.__name__}. Set the `polars_dtype` attribute for better specificity."
        )
        return pl.Object


FEATURE_CODEC = FeatureCodec()
