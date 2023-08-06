"""Type sla.enter, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal

from pydantic import BaseModel
from pydantic import validator

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class SlaEnter(BaseModel):
    TerminalAssetAlias: str  #
    TypeName: Literal["sla.enter"] = "sla.enter"
    Version: str = "000"

    _validator_terminal_asset_alias = predicate_validator(
        "TerminalAssetAlias", property_format.is_lrd_alias_format
    )

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class SlaEnter_Maker:
    type_name = "sla.enter"
    version = "000"

    def __init__(self, terminal_asset_alias: str):

        self.tuple = SlaEnter(
            TerminalAssetAlias=terminal_asset_alias,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: SlaEnter) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> SlaEnter:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> SlaEnter:
        d2 = dict(d)
        if "TerminalAssetAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TerminalAssetAlias")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return SlaEnter(
            TerminalAssetAlias=d2["TerminalAssetAlias"],
            TypeName=d2["TypeName"],
            Version="000",
        )
