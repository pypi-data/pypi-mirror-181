from typing import Annotated, TypeVar

T = TypeVar("T")


class PrimaryMeta(type):
    def __getitem__(self, item: T) -> Annotated[T, "primary"]:
        return Annotated[T, "__chalk_primary__"]


Primary = PrimaryMeta("Primary", (object,), {})
