"""Type basegnode.ctn.create, version 000"""
import json
from typing import Any
from typing import Dict
from typing import List
from typing import Literal

from pydantic import BaseModel
from pydantic import validator

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class BasegnodeCtnCreate(BaseModel):
    FromGNodeAlias: str  #
    FromGNodeInstanceId: str  #
    CtnGNodeAlias: str  #
    MicroLat: int  #
    MicroLon: int  #
    ChildAliasList: List[str]  #
    GNodeRegistryAddr: str  #
    TypeName: Literal["basegnode.ctn.create"] = "basegnode.ctn.create"
    Version: str = "000"

    _validator_from_g_node_alias = predicate_validator(
        "FromGNodeAlias", property_format.is_lrd_alias_format
    )

    _validator_from_g_node_instance_id = predicate_validator(
        "FromGNodeInstanceId", property_format.is_uuid_canonical_textual
    )

    _validator_ctn_g_node_alias = predicate_validator(
        "CtnGNodeAlias", property_format.is_lrd_alias_format
    )

    @validator("ChildAliasList")
    def _validator_child_alias_list(cls, v: List) -> List:
        for elt in v:
            if not property_format.is_lrd_alias_format(elt):
                raise ValueError(
                    f"failure of predicate is_lrd_alias_format() on elt {elt} of ChildAliasList"
                )
        return v

    _validator_g_node_registry_addr = predicate_validator(
        "GNodeRegistryAddr", property_format.is_algo_address_string_format
    )

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class BasegnodeCtnCreate_Maker:
    type_name = "basegnode.ctn.create"
    version = "000"

    def __init__(
        self,
        from_g_node_alias: str,
        from_g_node_instance_id: str,
        ctn_g_node_alias: str,
        micro_lat: int,
        micro_lon: int,
        child_alias_list: List[str],
        g_node_registry_addr: str,
    ):

        self.tuple = BasegnodeCtnCreate(
            FromGNodeAlias=from_g_node_alias,
            FromGNodeInstanceId=from_g_node_instance_id,
            CtnGNodeAlias=ctn_g_node_alias,
            MicroLat=micro_lat,
            MicroLon=micro_lon,
            ChildAliasList=child_alias_list,
            GNodeRegistryAddr=g_node_registry_addr,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: BasegnodeCtnCreate) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> BasegnodeCtnCreate:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> BasegnodeCtnCreate:
        d2 = dict(d)
        if "FromGNodeAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FromGNodeAlias")
        if "FromGNodeInstanceId" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FromGNodeInstanceId")
        if "CtnGNodeAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing CtnGNodeAlias")
        if "MicroLat" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MicroLat")
        if "MicroLon" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MicroLon")
        if "ChildAliasList" not in d2.keys():
            raise SchemaError(f"dict {d2} missing ChildAliasList")
        if "GNodeRegistryAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing GNodeRegistryAddr")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return BasegnodeCtnCreate(
            FromGNodeAlias=d2["FromGNodeAlias"],
            FromGNodeInstanceId=d2["FromGNodeInstanceId"],
            CtnGNodeAlias=d2["CtnGNodeAlias"],
            MicroLat=d2["MicroLat"],
            MicroLon=d2["MicroLon"],
            ChildAliasList=d2["ChildAliasList"],
            GNodeRegistryAddr=d2["GNodeRegistryAddr"],
            TypeName=d2["TypeName"],
            Version="000",
        )
