from enum import Enum


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return str(self.value)


class ValuesEnum(Enum):
    @classmethod
    def values(cls) -> list[str]:
        return [e.value for e in cls]
