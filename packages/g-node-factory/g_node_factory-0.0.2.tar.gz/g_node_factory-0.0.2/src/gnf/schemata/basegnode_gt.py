"""Type basegnode.gt, version 000"""
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
from gnf.data_classes import BaseGNode
from gnf.enums import CoreGNodeRole
from gnf.enums import GNodeStatus
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


class GNodeStatus100SchemaEnum:
    enum_name: str = "g.node.status.100"
    symbols: List[str] = [
        "00000000",
        "153d3475",
        "a2cfc2f7",
        "839b38db",
        "f5831e1d",
    ]

    @classmethod
    def is_symbol(cls, candidate: str) -> bool:
        if candidate in cls.symbols:
            return True
        return False


class GNodeStatus100(StrEnum):
    Unknown = auto()
    Pending = auto()
    Active = auto()
    PermanentlyDeactivated = auto()
    Suspended = auto()

    @classmethod
    def default(cls) -> "GNodeStatus100":
        return cls.Unknown

    @classmethod
    def values(cls) -> List[str]:
        return [elt.value for elt in cls]


class GNodeStatusMap:
    @classmethod
    def type_to_local(cls, symbol: str) -> GNodeStatus:
        if not GNodeStatus100SchemaEnum.is_symbol(symbol):
            raise SchemaError(f"{symbol} must belong to GNodeStatus100 symbols")
        versioned_enum = cls.type_to_versioned_enum_dict[symbol]
        return as_enum(versioned_enum, GNodeStatus, GNodeStatus.default())

    @classmethod
    def local_to_type(cls, g_node_status: GNodeStatus) -> str:
        if not isinstance(g_node_status, GNodeStatus):
            raise SchemaError(f"{g_node_status} must be of type {GNodeStatus}")
        versioned_enum = as_enum(
            g_node_status, GNodeStatus100, GNodeStatus100.default()
        )
        return cls.versioned_enum_to_type_dict[versioned_enum]

    type_to_versioned_enum_dict: Dict[str, GNodeStatus100] = {
        "00000000": GNodeStatus100.Unknown,
        "153d3475": GNodeStatus100.Pending,
        "a2cfc2f7": GNodeStatus100.Active,
        "839b38db": GNodeStatus100.PermanentlyDeactivated,
        "f5831e1d": GNodeStatus100.Suspended,
    }

    versioned_enum_to_type_dict: Dict[GNodeStatus100, str] = {
        GNodeStatus100.Unknown: "00000000",
        GNodeStatus100.Pending: "153d3475",
        GNodeStatus100.Active: "a2cfc2f7",
        GNodeStatus100.PermanentlyDeactivated: "839b38db",
        GNodeStatus100.Suspended: "f5831e1d",
    }


class BasegnodeGt(BaseModel):
    GNodeId: str  #
    Alias: str  #
    Status: GNodeStatus  #
    Role: CoreGNodeRole  #
    GNodeRegistryAddr: str  #
    PrevAlias: Optional[str] = None
    GpsPointId: Optional[str] = None
    OwnershipDeedNftId: Optional[int] = None
    OwnershipDeedValidatorAddr: Optional[str] = None
    OwnerAddr: Optional[str] = None
    DaemonAddr: Optional[str] = None
    TradingRightsNftId: Optional[int] = None
    TypeName: Literal["basegnode.gt"] = "basegnode.gt"
    Version: str = "000"

    _validator_g_node_id = predicate_validator(
        "GNodeId", property_format.is_uuid_canonical_textual
    )

    _validator_alias = predicate_validator("Alias", property_format.is_lrd_alias_format)

    @validator("Status")
    def _validator_status(cls, v: GNodeStatus) -> GNodeStatus:
        return as_enum(v, GNodeStatus, GNodeStatus.Unknown)

    @validator("Role")
    def _validator_role(cls, v: CoreGNodeRole) -> CoreGNodeRole:
        return as_enum(v, CoreGNodeRole, CoreGNodeRole.Other)

    _validator_g_node_registry_addr = predicate_validator(
        "GNodeRegistryAddr", property_format.is_algo_address_string_format
    )

    @validator("PrevAlias")
    def _validator_prev_alias(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not property_format.is_lrd_alias_format(v):
            raise ValueError(f"PrevAlias {v} must have LrdAliasFormat")
        return v

    @validator("GpsPointId")
    def _validator_gps_point_id(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not property_format.is_uuid_canonical_textual(v):
            raise ValueError(f"GpsPointId {v} must have UuidCanonicalTextual")
        return v

    @validator("OwnershipDeedNftId")
    def _validator_ownership_deed_nft_id(cls, v: Optional[int]) -> Optional[int]:
        if v is None:
            return v
        if not property_format.is_positive_integer(v):
            raise ValueError(f"OwnershipDeedNftId {v} must have PositiveInteger")
        return v

    @validator("OwnershipDeedValidatorAddr")
    def _validator_ownership_deed_validator_addr(
        cls, v: Optional[str]
    ) -> Optional[str]:
        if v is None:
            return v
        if not property_format.is_algo_address_string_format(v):
            raise ValueError(
                f"OwnershipDeedValidatorAddr {v} must have AlgoAddressStringFormat"
            )
        return v

    @validator("OwnerAddr")
    def _validator_owner_addr(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not property_format.is_algo_address_string_format(v):
            raise ValueError(f"OwnerAddr {v} must have AlgoAddressStringFormat")
        return v

    @validator("DaemonAddr")
    def _validator_daemon_addr(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not property_format.is_algo_address_string_format(v):
            raise ValueError(f"DaemonAddr {v} must have AlgoAddressStringFormat")
        return v

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        del d["Status"]
        Status = as_enum(self.Status, GNodeStatus, GNodeStatus.default())
        d["StatusGtEnumSymbol"] = GNodeStatusMap.local_to_type(Status)
        del d["Role"]
        Role = as_enum(self.Role, CoreGNodeRole, CoreGNodeRole.default())
        d["RoleGtEnumSymbol"] = CoreGNodeRoleMap.local_to_type(Role)
        if d["PrevAlias"] is None:
            del d["PrevAlias"]
        if d["GpsPointId"] is None:
            del d["GpsPointId"]
        if d["OwnershipDeedNftId"] is None:
            del d["OwnershipDeedNftId"]
        if d["OwnershipDeedValidatorAddr"] is None:
            del d["OwnershipDeedValidatorAddr"]
        if d["OwnerAddr"] is None:
            del d["OwnerAddr"]
        if d["DaemonAddr"] is None:
            del d["DaemonAddr"]
        if d["TradingRightsNftId"] is None:
            del d["TradingRightsNftId"]
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class BasegnodeGt_Maker:
    type_name = "basegnode.gt"
    version = "000"

    def __init__(
        self,
        g_node_id: str,
        alias: str,
        status: GNodeStatus,
        role: CoreGNodeRole,
        g_node_registry_addr: str,
        prev_alias: Optional[str],
        gps_point_id: Optional[str],
        ownership_deed_nft_id: Optional[int],
        ownership_deed_validator_addr: Optional[str],
        owner_addr: Optional[str],
        daemon_addr: Optional[str],
        trading_rights_nft_id: Optional[int],
    ):

        self.tuple = BasegnodeGt(
            GNodeId=g_node_id,
            Alias=alias,
            Status=status,
            Role=role,
            GNodeRegistryAddr=g_node_registry_addr,
            PrevAlias=prev_alias,
            GpsPointId=gps_point_id,
            OwnershipDeedNftId=ownership_deed_nft_id,
            OwnershipDeedValidatorAddr=ownership_deed_validator_addr,
            OwnerAddr=owner_addr,
            DaemonAddr=daemon_addr,
            TradingRightsNftId=trading_rights_nft_id,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: BasegnodeGt) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> BasegnodeGt:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> BasegnodeGt:
        d2 = dict(d)
        if "GNodeId" not in d2.keys():
            raise SchemaError(f"dict {d2} missing GNodeId")
        if "Alias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing Alias")
        if "StatusGtEnumSymbol" not in d2.keys():
            raise SchemaError(f"dict {d2} missing StatusGtEnumSymbol")
        if d2["StatusGtEnumSymbol"] in GNodeStatus100SchemaEnum.symbols:
            d2["Status"] = GNodeStatusMap.type_to_local(d2["StatusGtEnumSymbol"])
        else:
            d2["Status"] = GNodeStatus.default()
        if "RoleGtEnumSymbol" not in d2.keys():
            raise SchemaError(f"dict {d2} missing RoleGtEnumSymbol")
        if d2["RoleGtEnumSymbol"] in CoreGNodeRole000SchemaEnum.symbols:
            d2["Role"] = CoreGNodeRoleMap.type_to_local(d2["RoleGtEnumSymbol"])
        else:
            d2["Role"] = CoreGNodeRole.default()
        if "GNodeRegistryAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing GNodeRegistryAddr")
        if "PrevAlias" not in d2.keys():
            d2["PrevAlias"] = None
        if "GpsPointId" not in d2.keys():
            d2["GpsPointId"] = None
        if "OwnershipDeedNftId" not in d2.keys():
            d2["OwnershipDeedNftId"] = None
        if "OwnershipDeedValidatorAddr" not in d2.keys():
            d2["OwnershipDeedValidatorAddr"] = None
        if "OwnerAddr" not in d2.keys():
            d2["OwnerAddr"] = None
        if "DaemonAddr" not in d2.keys():
            d2["DaemonAddr"] = None
        if "TradingRightsNftId" not in d2.keys():
            d2["TradingRightsNftId"] = None
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return BasegnodeGt(
            GNodeId=d2["GNodeId"],
            Alias=d2["Alias"],
            Status=d2["Status"],
            Role=d2["Role"],
            GNodeRegistryAddr=d2["GNodeRegistryAddr"],
            PrevAlias=d2["PrevAlias"],
            GpsPointId=d2["GpsPointId"],
            OwnershipDeedNftId=d2["OwnershipDeedNftId"],
            OwnershipDeedValidatorAddr=d2["OwnershipDeedValidatorAddr"],
            OwnerAddr=d2["OwnerAddr"],
            DaemonAddr=d2["DaemonAddr"],
            TradingRightsNftId=d2["TradingRightsNftId"],
            TypeName=d2["TypeName"],
            Version="000",
        )

    @classmethod
    def tuple_to_dc(cls, t: BasegnodeGt) -> BaseGNode:
        if t.GNodeId in BaseGNode.by_id.keys():
            dc = BaseGNode.by_id[t.GNodeId]
        else:
            dc = BaseGNode(
                g_node_id=t.GNodeId,
                alias=t.Alias,
                status=t.Status,
                role=t.Role,
                g_node_registry_addr=t.GNodeRegistryAddr,
                prev_alias=t.PrevAlias,
                gps_point_id=t.GpsPointId,
                ownership_deed_nft_id=t.OwnershipDeedNftId,
                ownership_deed_validator_addr=t.OwnershipDeedValidatorAddr,
                owner_addr=t.OwnerAddr,
                daemon_addr=t.DaemonAddr,
                trading_rights_nft_id=t.TradingRightsNftId,
            )

        return dc

    @classmethod
    def dc_to_tuple(cls, dc: BaseGNode) -> BasegnodeGt:
        t = BasegnodeGt_Maker(
            g_node_id=dc.g_node_id,
            alias=dc.alias,
            status=dc.status,
            role=dc.role,
            g_node_registry_addr=dc.g_node_registry_addr,
            prev_alias=dc.prev_alias,
            gps_point_id=dc.gps_point_id,
            ownership_deed_nft_id=dc.ownership_deed_nft_id,
            ownership_deed_validator_addr=dc.ownership_deed_validator_addr,
            owner_addr=dc.owner_addr,
            daemon_addr=dc.daemon_addr,
            trading_rights_nft_id=dc.trading_rights_nft_id,
        ).tuple
        return t

    @classmethod
    def type_to_dc(cls, t: str) -> BaseGNode:
        return cls.tuple_to_dc(cls.type_to_tuple(t))

    @classmethod
    def dc_to_type(cls, dc: BaseGNode) -> str:
        return cls.dc_to_tuple(dc).as_type()

    @classmethod
    def dict_to_dc(cls, d: dict[Any, str]) -> BaseGNode:
        return cls.tuple_to_dc(cls.dict_to_tuple(d))
