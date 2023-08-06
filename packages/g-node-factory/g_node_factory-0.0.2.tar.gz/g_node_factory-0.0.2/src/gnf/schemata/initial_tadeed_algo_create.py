"""Type initial.tadeed.algo.create, version 000"""
import json
from typing import Dict
from typing import Literal

from pydantic import BaseModel

import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class InitialTadeedAlgoCreate(BaseModel):
    ValidatorAddr: str  #
    HalfSignedDeedCreationMtx: str  #
    TypeName: Literal["initial.tadeed.algo.create"] = "initial.tadeed.algo.create"
    Version: str = "000"

    _validator_validator_addr = predicate_validator(
        "ValidatorAddr", property_format.is_algo_address_string_format
    )

    _validator_half_signed_deed_creation_mtx = predicate_validator(
        "HalfSignedDeedCreationMtx", property_format.is_algo_msg_pack_encoded
    )

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class InitialTadeedAlgoCreate_Maker:
    type_name = "initial.tadeed.algo.create"
    version = "000"

    def __init__(self, validator_addr: str, half_signed_deed_creation_mtx: str):

        self.tuple = InitialTadeedAlgoCreate(
            ValidatorAddr=validator_addr,
            HalfSignedDeedCreationMtx=half_signed_deed_creation_mtx,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: InitialTadeedAlgoCreate) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> InitialTadeedAlgoCreate:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> InitialTadeedAlgoCreate:
        d2 = dict(d)
        if "ValidatorAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing ValidatorAddr")
        if "HalfSignedDeedCreationMtx" not in d2.keys():
            raise SchemaError(f"dict {d2} missing HalfSignedDeedCreationMtx")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return InitialTadeedAlgoCreate(
            ValidatorAddr=d2["ValidatorAddr"],
            HalfSignedDeedCreationMtx=d2["HalfSignedDeedCreationMtx"],
            TypeName=d2["TypeName"],
            Version="000",
        )
