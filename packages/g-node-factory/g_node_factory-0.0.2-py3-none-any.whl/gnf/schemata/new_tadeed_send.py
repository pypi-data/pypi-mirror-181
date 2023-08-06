"""Type new.tadeed.send, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal

from pydantic import BaseModel
from pydantic import validator

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class NewTadeedSend(BaseModel):
    NewTaDeedIdx: int  #
    OldTaDeedIdx: int  #
    TaDaemonAddr: str  #
    ValidatorAddr: str  #
    SignedTadeedOptinTxn: str  #
    TypeName: Literal["new.tadeed.send"] = "new.tadeed.send"
    Version: str = "000"

    _validator_ta_daemon_addr = predicate_validator(
        "TaDaemonAddr", property_format.is_algo_address_string_format
    )

    _validator_validator_addr = predicate_validator(
        "ValidatorAddr", property_format.is_algo_address_string_format
    )

    _validator_signed_tadeed_optin_txn = predicate_validator(
        "SignedTadeedOptinTxn", property_format.is_algo_msg_pack_encoded
    )

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class NewTadeedSend_Maker:
    type_name = "new.tadeed.send"
    version = "000"

    def __init__(
        self,
        new_ta_deed_idx: int,
        old_ta_deed_idx: int,
        ta_daemon_addr: str,
        validator_addr: str,
        signed_tadeed_optin_txn: str,
    ):

        self.tuple = NewTadeedSend(
            NewTaDeedIdx=new_ta_deed_idx,
            OldTaDeedIdx=old_ta_deed_idx,
            TaDaemonAddr=ta_daemon_addr,
            ValidatorAddr=validator_addr,
            SignedTadeedOptinTxn=signed_tadeed_optin_txn,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: NewTadeedSend) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> NewTadeedSend:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> NewTadeedSend:
        d2 = dict(d)
        if "NewTaDeedIdx" not in d2.keys():
            raise SchemaError(f"dict {d2} missing NewTaDeedIdx")
        if "OldTaDeedIdx" not in d2.keys():
            raise SchemaError(f"dict {d2} missing OldTaDeedIdx")
        if "TaDaemonAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaDaemonAddr")
        if "ValidatorAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing ValidatorAddr")
        if "SignedTadeedOptinTxn" not in d2.keys():
            raise SchemaError(f"dict {d2} missing SignedTadeedOptinTxn")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return NewTadeedSend(
            NewTaDeedIdx=d2["NewTaDeedIdx"],
            OldTaDeedIdx=d2["OldTaDeedIdx"],
            TaDaemonAddr=d2["TaDaemonAddr"],
            ValidatorAddr=d2["ValidatorAddr"],
            SignedTadeedOptinTxn=d2["SignedTadeedOptinTxn"],
            TypeName=d2["TypeName"],
            Version="000",
        )
