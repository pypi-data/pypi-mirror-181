"""Type tadeed.specs.hack, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal

from pydantic import BaseModel
from pydantic import validator

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class TadeedSpecsHack(BaseModel):
    TerminalAssetAlias: str  #
    MicroLat: int  #
    MicroLon: int  #
    DaemonPort: int  #
    TypeName: Literal["tadeed.specs.hack"] = "tadeed.specs.hack"
    Version: str = "000"

    _validator_terminal_asset_alias = predicate_validator(
        "TerminalAssetAlias", property_format.is_lrd_alias_format
    )

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class TadeedSpecsHack_Maker:
    type_name = "tadeed.specs.hack"
    version = "000"

    def __init__(
        self,
        terminal_asset_alias: str,
        micro_lat: int,
        micro_lon: int,
        daemon_port: int,
    ):

        self.tuple = TadeedSpecsHack(
            TerminalAssetAlias=terminal_asset_alias,
            MicroLat=micro_lat,
            MicroLon=micro_lon,
            DaemonPort=daemon_port,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: TadeedSpecsHack) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> TadeedSpecsHack:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> TadeedSpecsHack:
        d2 = dict(d)
        if "TerminalAssetAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TerminalAssetAlias")
        if "MicroLat" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MicroLat")
        if "MicroLon" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MicroLon")
        if "DaemonPort" not in d2.keys():
            raise SchemaError(f"dict {d2} missing DaemonPort")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return TadeedSpecsHack(
            TerminalAssetAlias=d2["TerminalAssetAlias"],
            MicroLat=d2["MicroLat"],
            MicroLon=d2["MicroLon"],
            DaemonPort=d2["DaemonPort"],
            TypeName=d2["TypeName"],
            Version="000",
        )
