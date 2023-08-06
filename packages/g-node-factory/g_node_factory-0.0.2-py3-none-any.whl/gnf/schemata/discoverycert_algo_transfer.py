"""Type discoverycert.algo.transfer, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal

from pydantic import BaseModel
from pydantic import validator

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class DiscoverycertAlgoTransfer(BaseModel):
    GNodeAlias: str  #
    DiscovererAddr: str  #
    TypeName: Literal["discoverycert.algo.transfer"] = "discoverycert.algo.transfer"
    Version: str = "000"

    _validator_g_node_alias = predicate_validator(
        "GNodeAlias", property_format.is_lrd_alias_format
    )

    _validator_discoverer_addr = predicate_validator(
        "DiscovererAddr", property_format.is_algo_address_string_format
    )

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class DiscoverycertAlgoTransfer_Maker:
    type_name = "discoverycert.algo.transfer"
    version = "000"

    def __init__(self, g_node_alias: str, discoverer_addr: str):

        self.tuple = DiscoverycertAlgoTransfer(
            GNodeAlias=g_node_alias,
            DiscovererAddr=discoverer_addr,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: DiscoverycertAlgoTransfer) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> DiscoverycertAlgoTransfer:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> DiscoverycertAlgoTransfer:
        d2 = dict(d)
        if "GNodeAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing GNodeAlias")
        if "DiscovererAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing DiscovererAddr")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return DiscoverycertAlgoTransfer(
            GNodeAlias=d2["GNodeAlias"],
            DiscovererAddr=d2["DiscovererAddr"],
            TypeName=d2["TypeName"],
            Version="000",
        )
