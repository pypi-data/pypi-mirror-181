"""Type terminalasset.certify.hack, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal

from pydantic import BaseModel
from pydantic import validator

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class TerminalassetCertifyHack(BaseModel):
    TerminalAssetAlias: str  #
    TaDaemonApiPort: str  #
    TaDaemonApiFqdn: str  #
    TaDaemonAddr: str  #
    TypeName: Literal["terminalasset.certify.hack"] = "terminalasset.certify.hack"
    Version: str = "000"

    _validator_terminal_asset_alias = predicate_validator(
        "TerminalAssetAlias", property_format.is_lrd_alias_format
    )

    _validator_ta_daemon_addr = predicate_validator(
        "TaDaemonAddr", property_format.is_algo_address_string_format
    )

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class TerminalassetCertifyHack_Maker:
    type_name = "terminalasset.certify.hack"
    version = "000"

    def __init__(
        self,
        terminal_asset_alias: str,
        ta_daemon_api_port: str,
        ta_daemon_api_fqdn: str,
        ta_daemon_addr: str,
    ):

        self.tuple = TerminalassetCertifyHack(
            TerminalAssetAlias=terminal_asset_alias,
            TaDaemonApiPort=ta_daemon_api_port,
            TaDaemonApiFqdn=ta_daemon_api_fqdn,
            TaDaemonAddr=ta_daemon_addr,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: TerminalassetCertifyHack) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> TerminalassetCertifyHack:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> TerminalassetCertifyHack:
        d2 = dict(d)
        if "TerminalAssetAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TerminalAssetAlias")
        if "TaDaemonApiPort" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaDaemonApiPort")
        if "TaDaemonApiFqdn" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaDaemonApiFqdn")
        if "TaDaemonAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaDaemonAddr")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return TerminalassetCertifyHack(
            TerminalAssetAlias=d2["TerminalAssetAlias"],
            TaDaemonApiPort=d2["TaDaemonApiPort"],
            TaDaemonApiFqdn=d2["TaDaemonApiFqdn"],
            TaDaemonAddr=d2["TaDaemonAddr"],
            TypeName=d2["TypeName"],
            Version="000",
        )
