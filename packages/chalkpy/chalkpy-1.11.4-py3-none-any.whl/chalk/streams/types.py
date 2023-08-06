from typing import Any, List, Sequence, Set, Type, Union

import polars
import pyarrow
from pydantic import BaseModel
from typing_extensions import TypeAlias

from chalk.features import DataFrame
from chalk.utils import AnyDataclass


class StreamResolverParam(BaseModel):
    name: str


class StreamResolverParamMessage(StreamResolverParam):
    typ: Union[Type[str], Type[bytes], Type[BaseModel], AnyDataclass]


StreamResolverWindowType: TypeAlias = Union[
    Type[List[str]],
    Type[List[bytes]],
    Type[List[BaseModel]],
    Type[AnyDataclass],
    Type[pyarrow.Table],
    Type[polars.DataFrame],
    Type[DataFrame],
    Any,  # The annotation value is likely going to be a GenericAlias, which messes with pydantic's validation
]


class StreamResolverParamMessageWindow(StreamResolverParam):
    typ: StreamResolverWindowType


class StreamResolverSignature(BaseModel):
    params: Sequence[StreamResolverParam]
    output_feature_fqns: Set[str]


class StreamResolverParamKeyedState(StreamResolverParam):
    typ: Union[Type[BaseModel], Type[AnyDataclass]]
    default_value: Any
