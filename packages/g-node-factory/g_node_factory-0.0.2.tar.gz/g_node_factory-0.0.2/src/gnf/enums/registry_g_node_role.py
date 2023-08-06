from enum import auto
from typing import List

from fastapi_utils.enums import StrEnum


class RegistryGNodeRole(StrEnum):
    Unknown = auto()
    GNodeFactory = auto()
    GNodeRegistry = auto()
    WorldInstanceRegistry = auto()
    World = auto()
    GridWorks = auto()

    @classmethod
    def default(cls) -> "RegistryGNodeRole":
        return cls.Unknown

    @classmethod
    def values(cls) -> List[str]:
        return [elt.value for elt in cls]
