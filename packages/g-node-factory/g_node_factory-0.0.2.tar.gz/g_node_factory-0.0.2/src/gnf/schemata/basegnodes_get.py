"""Type basegnodes.get, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal

from pydantic import BaseModel
from pydantic import validator

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class BasegnodesGet(BaseModel):
    TopGNodeAlias: str  #
    IncludeAllDescendants: bool  #
    FromGNodeAlias: str  #
    FromGNodeInstanceId: str  #
    TypeName: Literal["basegnodes.get"] = "basegnodes.get"
    Version: str = "000"

    _validator_top_g_node_alias = predicate_validator(
        "TopGNodeAlias", property_format.is_lrd_alias_format
    )

    _validator_from_g_node_alias = predicate_validator(
        "FromGNodeAlias", property_format.is_lrd_alias_format
    )

    _validator_from_g_node_instance_id = predicate_validator(
        "FromGNodeInstanceId", property_format.is_uuid_canonical_textual
    )

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class BasegnodesGet_Maker:
    type_name = "basegnodes.get"
    version = "000"

    def __init__(
        self,
        top_g_node_alias: str,
        include_all_descendants: bool,
        from_g_node_alias: str,
        from_g_node_instance_id: str,
    ):

        self.tuple = BasegnodesGet(
            TopGNodeAlias=top_g_node_alias,
            IncludeAllDescendants=include_all_descendants,
            FromGNodeAlias=from_g_node_alias,
            FromGNodeInstanceId=from_g_node_instance_id,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: BasegnodesGet) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> BasegnodesGet:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> BasegnodesGet:
        d2 = dict(d)
        if "TopGNodeAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TopGNodeAlias")
        if "IncludeAllDescendants" not in d2.keys():
            raise SchemaError(f"dict {d2} missing IncludeAllDescendants")
        if "FromGNodeAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FromGNodeAlias")
        if "FromGNodeInstanceId" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FromGNodeInstanceId")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return BasegnodesGet(
            TopGNodeAlias=d2["TopGNodeAlias"],
            IncludeAllDescendants=d2["IncludeAllDescendants"],
            FromGNodeAlias=d2["FromGNodeAlias"],
            FromGNodeInstanceId=d2["FromGNodeInstanceId"],
            TypeName=d2["TypeName"],
            Version="000",
        )
