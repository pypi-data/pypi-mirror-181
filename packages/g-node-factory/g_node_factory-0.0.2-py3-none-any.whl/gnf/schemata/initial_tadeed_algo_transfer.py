"""Type initial.tadeed.algo.transfer, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal

from pydantic import BaseModel
from pydantic import validator

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class InitialTadeedAlgoTransfer(BaseModel):
    MicroLat: int  #
    MicroLon: int  #
    ValidatorAddr: str  #
    TaDaemonAddr: str  #
    TaOwnerAddr: str  #
    FirstDeedTransferMtx: str  #
    TypeName: Literal["initial.tadeed.algo.transfer"] = "initial.tadeed.algo.transfer"
    Version: str = "000"

    _validator_validator_addr = predicate_validator(
        "ValidatorAddr", property_format.is_algo_address_string_format
    )

    _validator_ta_daemon_addr = predicate_validator(
        "TaDaemonAddr", property_format.is_algo_address_string_format
    )

    _validator_ta_owner_addr = predicate_validator(
        "TaOwnerAddr", property_format.is_algo_address_string_format
    )

    _validator_first_deed_transfer_mtx = predicate_validator(
        "FirstDeedTransferMtx", property_format.is_algo_msg_pack_encoded
    )

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class InitialTadeedAlgoTransfer_Maker:
    type_name = "initial.tadeed.algo.transfer"
    version = "000"

    def __init__(
        self,
        micro_lat: int,
        micro_lon: int,
        validator_addr: str,
        ta_daemon_addr: str,
        ta_owner_addr: str,
        first_deed_transfer_mtx: str,
    ):

        self.tuple = InitialTadeedAlgoTransfer(
            MicroLat=micro_lat,
            MicroLon=micro_lon,
            ValidatorAddr=validator_addr,
            TaDaemonAddr=ta_daemon_addr,
            TaOwnerAddr=ta_owner_addr,
            FirstDeedTransferMtx=first_deed_transfer_mtx,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: InitialTadeedAlgoTransfer) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> InitialTadeedAlgoTransfer:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> InitialTadeedAlgoTransfer:
        d2 = dict(d)
        if "MicroLat" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MicroLat")
        if "MicroLon" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MicroLon")
        if "ValidatorAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing ValidatorAddr")
        if "TaDaemonAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaDaemonAddr")
        if "TaOwnerAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaOwnerAddr")
        if "FirstDeedTransferMtx" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FirstDeedTransferMtx")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return InitialTadeedAlgoTransfer(
            MicroLat=d2["MicroLat"],
            MicroLon=d2["MicroLon"],
            ValidatorAddr=d2["ValidatorAddr"],
            TaDaemonAddr=d2["TaDaemonAddr"],
            TaOwnerAddr=d2["TaOwnerAddr"],
            FirstDeedTransferMtx=d2["FirstDeedTransferMtx"],
            TypeName=d2["TypeName"],
            Version="000",
        )
