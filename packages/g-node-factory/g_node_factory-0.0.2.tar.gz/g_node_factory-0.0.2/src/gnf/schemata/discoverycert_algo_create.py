"""Type discoverycert.algo.create, version 000"""
import json
from enum import auto
from typing import Any
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional

from fastapi_utils.enums import StrEnum
from pydantic import BaseModel
from pydantic import validator

import gnf.property_format as property_format
from gnf.enums import CoreGNodeRole
from gnf.errors import SchemaError
from gnf.message import as_enum
from gnf.property_format import predicate_validator


class CoreGNodeRole000SchemaEnum:
    enum_name: str = "core.g.node.role.000"
    symbols: List[str] = [
        "00000000",
        "0f8872f7",
        "9521af06",
        "d9823442",
        "86f21dd2",
        "4502e355",
        "d67e564e",
    ]

    @classmethod
    def is_symbol(cls, candidate: str) -> bool:
        if candidate in cls.symbols:
            return True
        return False


class CoreGNodeRole000(StrEnum):
    Other = auto()
    TerminalAsset = auto()
    AtomicMeteringNode = auto()
    AtomicTNode = auto()
    MarketMaker = auto()
    ConductorTopologyNode = auto()
    InterconnectionComponent = auto()

    @classmethod
    def default(cls) -> "CoreGNodeRole000":
        return cls.Other

    @classmethod
    def values(cls) -> List[str]:
        return [elt.value for elt in cls]


class CoreGNodeRoleMap:
    @classmethod
    def type_to_local(cls, symbol: str) -> CoreGNodeRole:
        if not CoreGNodeRole000SchemaEnum.is_symbol(symbol):
            raise SchemaError(f"{symbol} must belong to CoreGNodeRole000 symbols")
        versioned_enum = cls.type_to_versioned_enum_dict[symbol]
        return as_enum(versioned_enum, CoreGNodeRole, CoreGNodeRole.default())

    @classmethod
    def local_to_type(cls, core_g_node_role: CoreGNodeRole) -> str:
        if not isinstance(core_g_node_role, CoreGNodeRole):
            raise SchemaError(f"{core_g_node_role} must be of type {CoreGNodeRole}")
        versioned_enum = as_enum(
            core_g_node_role, CoreGNodeRole000, CoreGNodeRole000.default()
        )
        return cls.versioned_enum_to_type_dict[versioned_enum]

    type_to_versioned_enum_dict: Dict[str, CoreGNodeRole000] = {
        "00000000": CoreGNodeRole000.Other,
        "0f8872f7": CoreGNodeRole000.TerminalAsset,
        "9521af06": CoreGNodeRole000.AtomicMeteringNode,
        "d9823442": CoreGNodeRole000.AtomicTNode,
        "86f21dd2": CoreGNodeRole000.MarketMaker,
        "4502e355": CoreGNodeRole000.ConductorTopologyNode,
        "d67e564e": CoreGNodeRole000.InterconnectionComponent,
    }

    versioned_enum_to_type_dict: Dict[CoreGNodeRole000, str] = {
        CoreGNodeRole000.Other: "00000000",
        CoreGNodeRole000.TerminalAsset: "0f8872f7",
        CoreGNodeRole000.AtomicMeteringNode: "9521af06",
        CoreGNodeRole000.AtomicTNode: "d9823442",
        CoreGNodeRole000.MarketMaker: "86f21dd2",
        CoreGNodeRole000.ConductorTopologyNode: "4502e355",
        CoreGNodeRole000.InterconnectionComponent: "d67e564e",
    }


class DiscoverycertAlgoCreate(BaseModel):
    GNodeAlias: str  #
    CoreGNodeRole: CoreGNodeRole  #
    OldChildAliasList: List[str]  #
    DiscovererAddr: str  #
    SupportingMaterialHash: str  #
    MicroLat: Optional[int] = None
    MicroLon: Optional[int] = None
    TypeName: Literal["discoverycert.algo.create"] = "discoverycert.algo.create"
    Version: str = "000"

    _validator_g_node_alias = predicate_validator(
        "GNodeAlias", property_format.is_lrd_alias_format
    )

    @validator("CoreGNodeRole")
    def _validator_core_g_node_role(cls, v: CoreGNodeRole) -> CoreGNodeRole:
        return as_enum(v, CoreGNodeRole, CoreGNodeRole.Other)

    @validator("OldChildAliasList")
    def _validator_old_child_alias_list(cls, v: List) -> List:
        for elt in v:
            if not property_format.is_lrd_alias_format(elt):
                raise ValueError(
                    f"failure of predicate is_lrd_alias_format() on elt {elt} of OldChildAliasList"
                )
        return v

    _validator_discoverer_addr = predicate_validator(
        "DiscovererAddr", property_format.is_algo_address_string_format
    )

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        del d["CoreGNodeRole"]
        CoreGNodeRole = as_enum(
            self.CoreGNodeRole, CoreGNodeRole, CoreGNodeRole.default()
        )
        d["CoreGNodeRoleGtEnumSymbol"] = CoreGNodeRoleMap.local_to_type(CoreGNodeRole)
        if d["MicroLat"] is None:
            del d["MicroLat"]
        if d["MicroLon"] is None:
            del d["MicroLon"]
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class DiscoverycertAlgoCreate_Maker:
    type_name = "discoverycert.algo.create"
    version = "000"

    def __init__(
        self,
        g_node_alias: str,
        core_g_node_role: CoreGNodeRole,
        old_child_alias_list: List[str],
        discoverer_addr: str,
        supporting_material_hash: str,
        micro_lat: Optional[int],
        micro_lon: Optional[int],
    ):

        self.tuple = DiscoverycertAlgoCreate(
            GNodeAlias=g_node_alias,
            CoreGNodeRole=core_g_node_role,
            OldChildAliasList=old_child_alias_list,
            DiscovererAddr=discoverer_addr,
            SupportingMaterialHash=supporting_material_hash,
            MicroLat=micro_lat,
            MicroLon=micro_lon,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: DiscoverycertAlgoCreate) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> DiscoverycertAlgoCreate:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> DiscoverycertAlgoCreate:
        d2 = dict(d)
        if "GNodeAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing GNodeAlias")
        if "CoreGNodeRoleGtEnumSymbol" not in d2.keys():
            raise SchemaError(f"dict {d2} missing CoreGNodeRoleGtEnumSymbol")
        if d2["CoreGNodeRoleGtEnumSymbol"] in CoreGNodeRole000SchemaEnum.symbols:
            d2["CoreGNodeRole"] = CoreGNodeRoleMap.type_to_local(
                d2["CoreGNodeRoleGtEnumSymbol"]
            )
        else:
            d2["CoreGNodeRole"] = CoreGNodeRole.default()
        if "OldChildAliasList" not in d2.keys():
            raise SchemaError(f"dict {d2} missing OldChildAliasList")
        if "DiscovererAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing DiscovererAddr")
        if "SupportingMaterialHash" not in d2.keys():
            raise SchemaError(f"dict {d2} missing SupportingMaterialHash")
        if "MicroLat" not in d2.keys():
            d2["MicroLat"] = None
        if "MicroLon" not in d2.keys():
            d2["MicroLon"] = None
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return DiscoverycertAlgoCreate(
            GNodeAlias=d2["GNodeAlias"],
            CoreGNodeRole=d2["CoreGNodeRole"],
            OldChildAliasList=d2["OldChildAliasList"],
            DiscovererAddr=d2["DiscovererAddr"],
            SupportingMaterialHash=d2["SupportingMaterialHash"],
            MicroLat=d2["MicroLat"],
            MicroLon=d2["MicroLon"],
            TypeName=d2["TypeName"],
            Version="000",
        )
