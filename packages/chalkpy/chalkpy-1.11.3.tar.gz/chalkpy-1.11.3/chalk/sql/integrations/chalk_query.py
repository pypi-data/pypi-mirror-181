import time
from collections import defaultdict
from datetime import datetime
from enum import Enum
from typing import Any, List, Mapping, Optional, Sequence, Tuple, Union

from dateutil import parser
from sqlalchemy.engine.row import Row

from chalk.features import DataFrame, Feature, FeatureSetBase
from chalk.sql.base.protocols import BaseSQLSourceProtocol, ChalkQueryProtocol, DBSessionProtocol, IncrementalSettings
from chalk.utils.collections import get_unique_item
from chalk.utils.duration import Duration
from chalk.utils.log_with_context import get_logger
from chalk.utils.string import normalize_string_for_matching


class Finalizer(str, Enum):
    OneOrNone = "OneOrNone"
    One = "One"
    First = "First"
    All = "All"


_logger = get_logger(__name__)

# Fancy Python type for Sequence[str] that doesn't match against plain `str`s
StrSequence = Union[List[str], Tuple[str, ...]]


def _resolve_implicit_col_feature_mappings(
    explicit_mappings: Mapping[str, Feature],
    expected_features: Sequence[Feature],
    row_column_names: StrSequence,
) -> Sequence[Union[Feature, None]]:
    implicit_mappings = {normalize_string_for_matching(f.name): f for f in expected_features}
    return [
        explicit_mappings.get(col)
        if col in explicit_mappings
        else implicit_mappings.get(normalize_string_for_matching(col), None)
        for col in row_column_names
    ]


def _coerce_string_query_raw_value(feature: Feature, value: Any):
    if feature.typ is not None and issubclass(feature.typ.underlying, datetime) and isinstance(value, str):
        # Some SQL dialects/drivers, such as SQLite, will return datetimes as raw strings
        # TODO: there's no guarantee that this `value` is actually an ISO string. SQLite stores and returns them
        # in the format "%Y-%m-%d %H:%M:%S", which seems good enough for parser.isoparse()
        return parser.isoparse(value)

    return value


def _construct_features_single(
    col_feature_mappings: Sequence[Union[Feature, None]], row: Optional[Row], _coerce_raw_values: bool
):
    root_ns = get_unique_item((f.root_namespace for f in col_feature_mappings if f is not None), "root_ns")
    features_class = FeatureSetBase.registry[root_ns]

    if row is None:
        return features_class(**{f.attribute_name: None for f in col_feature_mappings if f is not None})

    assert len(row) == len(col_feature_mappings)
    return features_class(
        **{
            f.name: _coerce_string_query_raw_value(f, v) if _coerce_raw_values else v
            for (f, v) in zip(col_feature_mappings, row)
            if f is not None
        }
    )


def _construct_features_df(column_mapping: Sequence[Union[Feature, None]], rows: Sequence[Any]):
    # For client-facing sql execution, e.g. in tests, we go ahead and materialize the result set in memory
    data = defaultdict(list)
    for row in rows:
        for f, v in zip(column_mapping, row):
            if f is not None:
                data[f].append(v)

    return DataFrame(data)


class ChalkQuery(ChalkQueryProtocol):
    _session: DBSessionProtocol
    _source: BaseSQLSourceProtocol
    _features: List[Feature]
    _finalizer: Optional[Finalizer]
    _incremental_settings: Optional[Union[IncrementalSettings, bool]]

    def __init__(
        self,
        features: List[Feature],
        session: DBSessionProtocol,
        source: BaseSQLSourceProtocol,
        raw_session: Optional[Any] = None,
    ):
        self._session = session
        self._raw_session = raw_session or session
        self._features = features
        self._finalizer = None
        self._source = source
        self._incremental_settings = None

    def first(self):
        self._session.update_query(lambda x: x.limit(1))
        self._finalizer = Finalizer.First
        return self

    def one_or_none(self):
        self._session.update_query(lambda x: x.limit(1))
        self._finalizer = Finalizer.OneOrNone
        return self

    def one(self):
        self._session.update_query(lambda x: x.limit(1))
        self._finalizer = Finalizer.One
        return self

    def all(self):
        self._finalizer = Finalizer.All
        return self

    def incremental(
        self,
        lookback_period: Duration = "0s",
        incremental_column: Optional[Union[str, Feature]] = None,
        mode: str = "row",
    ):
        self._finalizer = Finalizer.All
        self._incremental_settings = IncrementalSettings(
            lookback_period=lookback_period, incremental_column=incremental_column, mode=mode
        )
        return self

    def filter_by(self, **kwargs):
        self._session.update_query(lambda x: x.filter_by(**kwargs))
        return self

    def filter(self, *criterion):
        self._session.update_query(lambda x: x.filter(*criterion))
        return self

    def limit(self, *limits):
        self._session.update_query(lambda x: x.limit(*limits))
        return self

    def order_by(self, *clauses):
        self._session.update_query(lambda x: x.order_by(*clauses))
        return self

    def group_by(self, *clauses):
        self._session.update_query(lambda x: x.group_by(*clauses))
        return self

    def having(self, criterion):
        self._session.update_query(lambda x: x.having(*criterion))
        return self

    def union(self, *q):
        self._session.update_query(lambda x: x.union(*q))
        return self

    def union_all(self, *q):
        self._session.update_query(lambda x: x.union_all(*q))
        return self

    def intersect(self, *q):
        self._session.update_query(lambda x: x.intersect(*q))
        return self

    def intersect_all(self, *q):
        self._session.update_query(lambda x: x.intersect_all(*q))
        return self

    def join(self, target, *props, **kwargs):
        self._session.update_query(lambda x: x.join(target, *props, **kwargs))
        return self

    def outerjoin(self, target, *props, **kwargs):
        self._session.update_query(lambda x: x.outerjoin(target, *props, **kwargs))
        return self

    def select_from(self, *from_obj):
        self._session.update_query(lambda x: x.select_from(*from_obj))
        return self

    @staticmethod
    def _get_finalizer_fn(f: Optional[Finalizer]):
        if f == Finalizer.First:
            return lambda x: x.first()
        if f == Finalizer.All:
            return lambda x: x.all()
        if f == Finalizer.One:
            return lambda x: x.one()
        if f == Finalizer.OneOrNone:
            return lambda x: x.one_or_none()
        if f is None:
            return lambda x: x.all()
        raise ValueError(f"Unknown finalizer {f}")

    def execute(self):
        return self.execute_internal(expected_features=[])

    def execute_internal(self, *, expected_features: Sequence[Feature]):
        start = time.perf_counter()
        try:
            col_names = [d["name"] for d in self._session._session.column_descriptions]
            self._session.update_query(self._get_finalizer_fn(self._finalizer))
            tuples = self._session.result()
            self._raw_session.close()

            fqn_to_feature = {f.fqn: f for f in self._features}
            cols = [fqn_to_feature[c] for c in col_names if c in fqn_to_feature]

            if isinstance(tuples, list):
                lists = defaultdict(list)

                for tuple in tuples:
                    for col_i, x in enumerate(tuple):
                        if isinstance(x, Enum):
                            x = x.value
                        lists[col_i].append(x)
                return DataFrame({col: lists[i] for i, col in enumerate(cols)})

            return _construct_features_single(cols, tuples, _coerce_raw_values=False)
        finally:
            _logger.debug(f"query.execute: {time.perf_counter() - start}")
