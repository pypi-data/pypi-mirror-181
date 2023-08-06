from enum import auto
from typing import List

from fastapi_utils.enums import StrEnum


class CoreGNodeRole(StrEnum):
    Other = auto()
    TerminalAsset = auto()
    AtomicMeteringNode = auto()
    AtomicTNode = auto()
    MarketMaker = auto()
    ConductorTopologyNode = auto()
    InterconnectionComponent = auto()

    @classmethod
    def default(cls) -> "CoreGNodeRole":
        return cls.Other

    @classmethod
    def values(cls) -> List[str]:
        return [elt.value for elt in cls]
