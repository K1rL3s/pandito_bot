from enum import Enum
from typing import TypeVar

T = TypeVar("T")


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return str(self.value)


class ValuesEnum(Enum):
    @classmethod
    def values(cls) -> list[T]:
        return [e.value for e in cls]
