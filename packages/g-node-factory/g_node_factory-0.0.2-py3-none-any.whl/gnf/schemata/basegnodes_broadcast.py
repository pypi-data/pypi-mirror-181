"""Type basegnodes.broadcast, version 000"""
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
from gnf.schemata.basegnode_gt import BasegnodeGt
from gnf.schemata.basegnode_gt import BasegnodeGt_Maker


class BasegnodesBroadcast(BaseModel):
    FromGNodeAlias: str  #
    FromGNodeInstanceId: str  #
    IncludeAllDescendants: bool  #
    TopGNode: BasegnodeGt  #
    DescendantGNodeList: List[BasegnodeGt]
    # TypeName: Literal["basegnodes.broadcast"] = "basegnodes.broadcast"
    Version: str = "000"

    _validator_from_g_node_alias = predicate_validator(
        "FromGNodeAlias", property_format.is_lrd_alias_format
    )

    _validator_from_g_node_instance_id = predicate_validator(
        "FromGNodeInstanceId", property_format.is_uuid_canonical_textual
    )

    @validator("DescendantGNodeList")
    def _validator_descendant_g_node_list(cls, v: List) -> List:
        for elt in v:
            if not isinstance(elt, BasegnodeGt):
                raise ValueError(
                    f"elt {elt} of DescendantGNodeList must have type BasegnodeGt."
                )
        return v

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        d["TopGNode"] = self.TopGNode.as_dict()

        # Recursively call as_dict() for the SubTypes
        descendant_g_node_list = []
        for elt in self.DescendantGNodeList:
            descendant_g_node_list.append(elt.as_dict())
        d["DescendantGNodeList"] = descendant_g_node_list
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class BasegnodesBroadcast_Maker:
    type_name = "basegnodes.broadcast"
    version = "000"

    def __init__(
        self,
        from_g_node_alias: str,
        from_g_node_instance_id: str,
        include_all_descendants: bool,
        top_g_node: BasegnodeGt,
        descendant_g_node_list: List[BasegnodeGt],
    ):

        self.tuple = BasegnodesBroadcast(
            FromGNodeAlias=from_g_node_alias,
            FromGNodeInstanceId=from_g_node_instance_id,
            IncludeAllDescendants=include_all_descendants,
            TopGNode=top_g_node,
            DescendantGNodeList=descendant_g_node_list,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: BasegnodesBroadcast) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> BasegnodesBroadcast:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> BasegnodesBroadcast:
        d2 = dict(d)
        if "FromGNodeAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FromGNodeAlias")
        if "FromGNodeInstanceId" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FromGNodeInstanceId")
        if "IncludeAllDescendants" not in d2.keys():
            raise SchemaError(f"dict {d2} missing IncludeAllDescendants")
        if "TopGNode" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TopGNode")
        if not isinstance(d2["TopGNode"], dict):
            raise SchemaError(f"d['TopGNode'] {d2['TopGNode']} must be a BasegnodeGt!")
        top_g_node = BasegnodeGt_Maker.dict_to_tuple(d2["TopGNode"])
        d2["TopGNode"] = top_g_node
        if "DescendantGNodeList" not in d2.keys():
            raise SchemaError(f"dict {d2} missing DescendantGNodeList")
        descendant_g_node_list = []
        if not isinstance(d2["DescendantGNodeList"], List):
            raise SchemaError("DescendantGNodeList must be a List!")
        for elt in d2["DescendantGNodeList"]:
            if not isinstance(elt, dict):
                raise SchemaError(
                    f"elt {elt} of DescendantGNodeList must be "
                    "BasegnodeGt but not even a dict!"
                )
            descendant_g_node_list.append(BasegnodeGt_Maker.dict_to_tuple(elt))
        d2["DescendantGNodeList"] = descendant_g_node_list
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return BasegnodesBroadcast(
            FromGNodeAlias=d2["FromGNodeAlias"],
            FromGNodeInstanceId=d2["FromGNodeInstanceId"],
            IncludeAllDescendants=d2["IncludeAllDescendants"],
            TopGNode=d2["TopGNode"],
            DescendantGNodeList=d2["DescendantGNodeList"],
            TypeName=d2["TypeName"],
            Version="000",
        )
