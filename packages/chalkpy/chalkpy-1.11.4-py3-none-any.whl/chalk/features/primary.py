from typing import Annotated, TypeVar

T = TypeVar("T")


class PrimaryMeta(type):
    def __getitem__(self, item: T) -> Annotated[T, "primary"]:
        return Annotated[T, "primary"]


Primary = PrimaryMeta("Primary", (object,), {})
