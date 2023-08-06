"""Type tavalidatorcert.algo.transfer, version 000"""
import json
from typing import Any
from typing import Dict
from typing import List
from typing import Literal
from typing import OrderedDict

import dotenv
from algosdk import encoding
from algosdk.future.transaction import AssetTransferTxn
from algosdk.future.transaction import MultisigTransaction
from algosdk.v2client.algod import AlgodClient
from pydantic import BaseModel
from pydantic import root_validator

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class TavalidatorcertAlgoTransfer(BaseModel):
    ValidatorAddr: str  #
    HalfSignedCertTransferMtx: str  #
    TypeName: Literal["tavalidatorcert.algo.transfer"] = "tavalidatorcert.algo.transfer"
    Version: str = "000"

    _validator_validator_addr = predicate_validator(
        "ValidatorAddr", property_format.is_algo_address_string_format
    )

    _validator_half_signed_cert_transfer_mtx = predicate_validator(
        "HalfSignedCertTransferMtx", property_format.is_algo_msg_pack_encoded
    )

    @root_validator(pre=True)
    def _axioms_1_and_2(cls, v) -> Any:
        """Axiom 1: Decoded HalfSignedCertTransferMtx  must have type MultisigTransaction.
        Axiom 2: The HalfSignedCertTransferMtx.txn must have type AssetTransferTxn"""
        mtx = encoding.future_msgpack_decode(v.get("HalfSignedCertTransferMtx", None))
        txn = mtx.transaction
        if not isinstance(mtx, MultisigTransaction):
            raise ValueError(
                "Axiom 1: Decoded HalfSignedCertTransferMtx must have type MultisigTransaction,"
                f" got {type(mtx)}"
            )
        if not isinstance(txn, AssetTransferTxn):
            raise ValueError(
                "Axiom 2: The HalfSignedCertTransferMtx.txn must have type AssetTransferTxn,"
                f" got {type(txn)}"
            )

        return v

    @root_validator
    def _axiom_3(cls, v) -> Any:
        """Axiom 3: The HalfSignedCertCreationMtx MultiSig must be the 1-sig TaMulti
        [Gnf Admin, payload.ValidatorAddr]"""
        mtx = encoding.future_msgpack_decode(v.get("HalfSignedCertTransferMtx", None))
        msig = mtx.multisig
        ValidatorAddr = v.get("ValidatorAddr", None)
        gnf_admin_addr = config.GnfPublic().gnf_admin_addr
        multi = algo_utils.MultisigAccount(
            version=1,
            threshold=2,
            addresses=[gnf_admin_addr, ValidatorAddr],
        )
        if msig.address() != multi.addr:
            raise ValueError(
                f"Axiom 3: The HalfSignedCertCreationMtx MultiSig must be the 1-sig TaMulti"
                "[Gnf Admin, payload.ValidatorAddr].\nGot {msig.address()}.\nExpected {multi.addr}"
            )

        return v

    @root_validator
    def _axiom_4(cls, v) -> Any:
        """Axiom 4: The Transfer asset-index must be for the existing Validator Certificate
        co-created by the multi account"""
        mtx = encoding.future_msgpack_decode(v.get("HalfSignedCertTransferMtx", None))
        txn = mtx.transaction
        ValidatorAddr = v.get("ValidatorAddr", None)
        od: OrderedDict = txn.dictify()
        transfer_asset_idx = od["xaid"]
        validator_cert_idx = api_utils.get_validator_cert_idx(ValidatorAddr)
        if transfer_asset_idx != validator_cert_idx:
            raise ValueError(
                "Axiom 4: The Transfer asset-index must be for the existing Validator Certificate"
                "co-created by the multi account. Transfer request is for asset-index"
                f" {transfer_asset_idx} but the Validator Certificate idx is {validator_cert_idx}!"
            )
        return v

    @root_validator
    def _axiom_5(cls, v) -> Any:
        """Axiom 5: For the asset transfer: receiver is validator, sender is validator multi,
        transfer amount is 1"""
        mtx = encoding.future_msgpack_decode(v.get("HalfSignedCertTransferMtx", None))
        txn = mtx.transaction
        ValidatorAddr = v.get("ValidatorAddr", None)
        od: OrderedDict = txn.dictify()
        validator_pk = encoding.decode_address(ValidatorAddr)
        if od["arcv"] != validator_pk:
            raise ValueError(
                "Axiom 5: Receiver should be ValidatorAddr (encoding.decode_address(ValidatorAddress)),"
                " not {od['arcv']} "
            )
        gnf_admin_addr = config.GnfPublic().gnf_admin_addr
        multi = algo_utils.MultisigAccount(
            version=1,
            threshold=2,
            addresses=[gnf_admin_addr, ValidatorAddr],
        )
        multi_pk = encoding.decode_address(multi.addr)
        if od["snd"] != multi_pk:
            raise ValueError(
                f"Axiom 5: Sender should be 2-sig [GnfAdmin, Validator] multi, not {od['snd']}"
            )

        # Check that the transfer request amount is 1
        if od["aamt"] != 1:
            raise ValueError(
                f"Axiom 5: transfer request should be 1, not {od['aamt']} "
            )
        return v

    @root_validator
    def _axiom_6(cls, v) -> Any:
        """Axiom 6: Validator multi must have enough algos"""
        ValidatorAddr = v.get("ValidatorAddr", None)
        try:
            api_utils.check_validator_multi_has_enough_algos(ValidatorAddr)
        except SchemaError as e:
            raise ValueError(e)
        return v

    @root_validator
    def _axiom_7(cls, v) -> Any:
        """Axiom 7: ValidatorAddr must have opted into the certificate, and the multi account must
        still own the certificate"""
        mtx = encoding.future_msgpack_decode(v.get("HalfSignedCertTransferMtx", None))
        txn = mtx.transaction
        ValidatorAddr = v.get("ValidatorAddr", None)
        od: OrderedDict = txn.dictify()
        asset_index = od["xaid"]
        settings = config.VanillaSettings(_env_file=dotenv.find_dotenv())
        client: AlgodClient = AlgodClient(
            settings.algo_api_secrets.algod_token.get_secret_value(),
            settings.public.algod_address,
        )
        validator_assets = client.account_info(ValidatorAddr)["assets"]
        if (
            len(list(filter(lambda x: x["asset-id"] == asset_index, validator_assets)))
            == 0
        ):
            raise ValueError(
                f"Axiom 7: ValidatorAddr {ValidatorAddr} has not opted in to certificate"
                f" {asset_index}"
            )
        gnf_admin_addr = config.GnfPublic().gnf_admin_addr
        multi = algo_utils.MultisigAccount(
            version=1,
            threshold=2,
            addresses=[gnf_admin_addr, ValidatorAddr],
        )
        multi_assets = client.account_info(multi.addr)["assets"]
        if len(list(filter(lambda x: x["asset-id"] == asset_index, multi_assets))) == 0:
            raise ValueError(
                f"Axiom 7:  multiasset  {multi.addr} never owned {asset_index}!"
            )

        this_asset_dict: OrderedDict = list(
            filter(lambda x: x["asset-id"] == asset_index, multi_assets)
        )[0]
        if this_asset_dict["amount"] == 0:
            raise ValueError(
                f"Axiom 7:  multiasset  {multi.addr} no longer owns {asset_index}!"
            )
        return v

    @root_validator
    def _axiom_8(cls, v) -> Any:
        """Axiom 8: ValidatorAddr must have signed the mtx"""
        mtx = encoding.future_msgpack_decode(v.get("HalfSignedCertTransferMtx", None))
        ValidatorAddr = v.get("ValidatorAddr", None)
        try:
            api_utils.check_mtx_subsig(mtx, ValidatorAddr)
        except SchemaError as e:
            raise ValueError(f"Axiom 5: ValidatorAddr must have signed the mtx: {e}")
        return v

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class TavalidatorcertAlgoTransfer_Maker:
    type_name = "tavalidatorcert.algo.transfer"
    version = "000"

    def __init__(self, validator_addr: str, half_signed_cert_transfer_mtx: str):

        self.tuple = TavalidatorcertAlgoTransfer(
            ValidatorAddr=validator_addr,
            HalfSignedCertTransferMtx=half_signed_cert_transfer_mtx,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: TavalidatorcertAlgoTransfer) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> TavalidatorcertAlgoTransfer:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> TavalidatorcertAlgoTransfer:
        d2 = dict(d)
        if "ValidatorAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing ValidatorAddr")
        if "HalfSignedCertTransferMtx" not in d2.keys():
            raise SchemaError(f"dict {d2} missing HalfSignedCertTransferMtx")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return TavalidatorcertAlgoTransfer(
            ValidatorAddr=d2["ValidatorAddr"],
            HalfSignedCertTransferMtx=d2["HalfSignedCertTransferMtx"],
            TypeName=d2["TypeName"],
            Version="000",
        )
