"""Type basegnode.other.create, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal

from pydantic import BaseModel
from pydantic import validator

from gnf.errors import SchemaError


class BasegnodeOtherCreate(BaseModel):
    TypeName: Literal["basegnode.other.create"] = "basegnode.other.create"
    Version: str = "000"

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class BasegnodeOtherCreate_Maker:
    type_name = "basegnode.other.create"
    version = "000"

    def __init__(self):

        self.tuple = BasegnodeOtherCreate(
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: BasegnodeOtherCreate) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> BasegnodeOtherCreate:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> BasegnodeOtherCreate:
        d2 = dict(d)
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return BasegnodeOtherCreate(
            TypeName=d2["TypeName"],
            Version="000",
        )
