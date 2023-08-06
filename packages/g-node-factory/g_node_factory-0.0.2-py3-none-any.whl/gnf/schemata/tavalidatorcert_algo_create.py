"""Type tavalidatorcert.algo.create, version 000"""
import json
from typing import Any
from typing import Dict
from typing import List
from typing import Literal
from typing import OrderedDict

import algosdk
from algosdk import encoding
from algosdk.future import transaction
from pydantic import BaseModel
from pydantic import root_validator

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class TavalidatorcertAlgoCreate(BaseModel):
    ValidatorAddr: str  #
    HalfSignedCertCreationMtx: str  #
    TypeName: Literal["tavalidatorcert.algo.create"] = "tavalidatorcert.algo.create"
    Version: str = "000"

    _validator_validator_addr = predicate_validator(
        "ValidatorAddr", property_format.is_algo_address_string_format
    )

    _validator_half_signed_cert_creation_mtx = predicate_validator(
        "HalfSignedCertCreationMtx", property_format.is_algo_msg_pack_encoded
    )

    @root_validator(pre=True)
    def _axioms_1_and_2(cls, v) -> Any:
        """Axiom 1: Decoded HalfSignedDeedCreationMtx must have type MultisigTransaction.
        Axiom 2:  The HalfSignedDeedCreationMtx.txn must have type AssetConfigTxn"""
        mtx = encoding.future_msgpack_decode(v.get("HalfSignedCertCreationMtx", None))
        if not isinstance(mtx, transaction.MultisigTransaction):
            raise ValueError(
                "Axiom 1: Decoded HalfSignedDeedCreationMtx must have type MultisigTransaction,"
                f" got {type(mtx)}"
            )
        txn = mtx.transaction
        if not isinstance(txn, transaction.AssetConfigTxn):
            raise ValueError(
                f"Axiom 2: The HalfSignedDeedCreationMtx.txn must have type AssetConfigTxn, got {type(txn)}"
            )
        return v

    @root_validator
    def _axiom_3(cls, v) -> Any:
        """Axiom 3: The HalfSignedCertCreationMtx MultiSig must be the 2-sig Multi [Gnf Admin, payload.ValidatorAddr]"""
        mtx = encoding.future_msgpack_decode(v.get("HalfSignedCertCreationMtx", None))
        msig = mtx.multisig
        gnf_admin_addr = config.GnfPublic().gnf_admin_addr
        ValidatorAddr = v.get("ValidatorAddr")
        multi = algo_utils.MultisigAccount(
            version=1,
            threshold=2,
            addresses=[gnf_admin_addr, ValidatorAddr],
        )
        if msig.address() != multi.addr:
            raise ValueError(
                f"Axiom 3: The HalfSignedCertCreationMtx MultiSig must be the 2-sig Multi [Gnf Admin, payload.ValidatorAddr].\nGot {msig.address()}.\nExpected {multi.addr}"
            )

        return v

    @root_validator
    def _axiom_4(cls, v) -> Any:
        """Axiom 4: For the asset getting created: total = 1, unit_name=VLDTR, manager is Gnf Admin, asset_name and url not blank."""
        mtx = encoding.future_msgpack_decode(v.get("HalfSignedCertCreationMtx", None))
        txn = mtx.transaction
        gnf_admin_addr = config.GnfPublic().gnf_admin_addr
        od = txn.dictify()
        try:
            apar: OrderedDict = od["apar"]
        except:
            raise Exception(
                "Unexpected error. AssetCreationTxn.dictify() did not have 'apar' key"
            )
        if apar["t"] != 1:
            raise ValueError(
                f"Axiom 4: notValidatorCertFormat - total must be 1, not {apar['t']}"
            )
        if apar["un"] != "VLDTR":
            raise ValueError(
                f"Axiom 4: notValidatorCertFormat - unit_name must be VLDTR, not {apar['un']}"
            )
        if apar["m"] != algosdk.encoding.decode_address(gnf_admin_addr):
            raise ValueError(
                f"Axiom 4: notValidatorCertFormat - manager must be ..{gnf_admin_addr[-6:]}"
            )
        if "an" not in apar.keys():
            raise ValueError("Axiom 4: asset-name must exist")
        if "au" not in apar.keys():
            raise ValueError("Axiom 4: url must exist")
        return v

    @root_validator
    def _axiom_5(cls, v) -> Any:
        """Axiom 5: ValidatorAddr must have signed the HalfSignedCertCreationMtx"""
        mtx = encoding.future_msgpack_decode(v.get("HalfSignedCertCreationMtx", None))
        ValidatorAddr = v.get("ValidatorAddr")
        try:
            api_utils.check_mtx_subsig(mtx, ValidatorAddr)
        except SchemaError as e:
            raise ValueError(
                f"Axiom 5: ValidatorAddr must have signed the HalfSignedCertCreationMtx: {e}"
            )
        return v

    @root_validator
    def _axiom_6(cls, v) -> Any:
        """Axiom 6: There must not already be a ValidatorCert in the 2-sig
        [Gnf Admin, ValidatorAddr] acct."""
        ValidatorAddr = v.get("ValidatorAddr")
        existing_cert_idx = api_utils.get_validator_cert_idx(
            validator_addr=ValidatorAddr
        )
        if existing_cert_idx:
            raise ValueError(
                "Axiom 6: There must not already be a ValidatorCert in the 2-sig [Gnf Admin, "
                f" ValidatorAddr] acct. Found {existing_cert_idx}"
            )
        return v

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())

    def __repr__(self):
        r = "CreateTavalidatorcertAlgo"
        r += f"\n   API TypeName: {self.TypeName}"
        r += f"\n   ValidatorAddr: {self.ValidatorAddr}"
        mtx = algosdk.encoding.future_msgpack_decode(self.HalfSignedCertCreationMtx)
        msig = mtx.multisig
        sender = msig.address()
        apar = mtx.transaction.dictify()["apar"]
        total = apar["t"]
        unit_name = apar["un"]
        manager = algosdk.encoding.encode_address(apar["m"])
        url = apar["au"]
        asset_name = apar["an"]
        r += "\n   HalfSignedCertCreationMtx - encoding of a half-signed mtx for this AssetCreationTransaction:"
        r += f"\n       sender=..{sender[-6:]}"
        r += f"\n       total={total}"
        r += "\n       decimals=0"
        r += f"\n       manager=..{manager[-6:]}"
        r += f"\n       asset_name={asset_name}"
        r += f"\n       unit_name={unit_name}"
        r += f"\n       url={url}"

        return r


class TavalidatorcertAlgoCreate_Maker:
    type_name = "tavalidatorcert.algo.create"
    version = "000"

    def __init__(self, validator_addr: str, half_signed_cert_creation_mtx: str):

        self.tuple = TavalidatorcertAlgoCreate(
            ValidatorAddr=validator_addr,
            HalfSignedCertCreationMtx=half_signed_cert_creation_mtx,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: TavalidatorcertAlgoCreate) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> TavalidatorcertAlgoCreate:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> TavalidatorcertAlgoCreate:
        d2 = dict(d)
        if "ValidatorAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing ValidatorAddr")
        if "HalfSignedCertCreationMtx" not in d2.keys():
            raise SchemaError(f"dict {d2} missing HalfSignedCertCreationMtx")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return TavalidatorcertAlgoCreate(
            ValidatorAddr=d2["ValidatorAddr"],
            HalfSignedCertCreationMtx=d2["HalfSignedCertCreationMtx"],
            TypeName=d2["TypeName"],
            Version="000",
        )
