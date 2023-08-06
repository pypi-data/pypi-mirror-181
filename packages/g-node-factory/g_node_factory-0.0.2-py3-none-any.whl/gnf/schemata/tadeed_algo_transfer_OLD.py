"""Type tadeed.algo.transfer, version 000"""
import json
from typing import Any
from typing import Dict
from typing import List
from typing import Literal
from typing import NamedTuple

import dotenv
from algosdk import encoding
from algosdk.future import transaction
from algosdk.future.transaction import AssetTransferTxn
from algosdk.v2client.algod import AlgodClient
from pydantic import BaseModel
from pydantic import root_validator

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
import gnf.property_format as property_format
from gnf.algo_utils import MultisigAccount
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class TadeedAlgoTransfer(BaseModel):
    FirstDeedTransferMtx: str  #
    MicroLat: int  #
    DeedValidatorAddr: str  #
    TaDaemonAddr: str  #
    TaOwnerAddr: str  #
    MicroLon: int  #
    TypeName: Literal["tadeed.algo.transfer"] = "tadeed.algo.transfer"
    Version: str = "000"

    _validator_first_deed_transfer_mtx = predicate_validator(
        "FirstDeedTransferMtx", property_format.is_algo_msg_pack_encoded
    )

    _validator_deed_validator_addr = predicate_validator(
        "DeedValidatorAddr", property_format.is_algo_address_string_format
    )

    _validator_ta_daemon_addr = predicate_validator(
        "TaDaemonAddr", property_format.is_algo_address_string_format
    )

    _validator_ta_owner_addr = predicate_validator(
        "TaOwnerAddr", property_format.is_algo_address_string_format
    )

    @root_validator(pre=True)
    def _axioms_1_and_2(cls, v) -> Any:
        """Axiom 1: Decoded FirstDeedTransferMtx must have type MultisigTransaction.
        Axiom 2: The FirstDeedTransferMtx.txn must have type AssetTransferTxn"""
        mtx = encoding.future_msgpack_decode(v.get("FirstDeedTransferMtx", None))
        txn = mtx.transaction
        if not isinstance(mtx, transaction.MultisigTransaction):
            raise ValueError(
                "Axiom 1: Decoded FirstDeedTransferMtx must have type MultisigTransaction,"
                f" got {type(mtx)}"
            )
        if not isinstance(txn, AssetTransferTxn):
            raise ValueError(
                "Axiom 2: The FirstDeedTransferMtx.txn must have type AssetTransferTxn,"
                f" got {type(txn)}"
            )

        return v

    @root_validator
    def _axiom_3(cls, v) -> Any:
        """Axiom 3: The MultiSig must belong to the 2-sig Multi [Gnf Admin, payload.DeedValidatorAddr]"""
        mtx = encoding.future_msgpack_decode(v.get("FirstDeedTransferMtx", None))
        msig = mtx.multisig
        DeedValidatorAddr = v.get("DeedValidatorAddr", None)
        gnf_admin_addr = config.GnfPublic().gnf_admin_addr
        multi = MultisigAccount(
            version=1,
            threshold=2,
            addresses=[gnf_admin_addr, DeedValidatorAddr],
        )
        if msig.address() != multi.addr:
            raise ValueError(
                "Axiom 3: The MultiSig must belong to the 2-sig Multi "
                f"[Gnf Admin, payload.DeedValidatorAddr]. Got {msig.address()[-6:]}. Expected {multi.addr[-6:]}"
            )

        return v

    @root_validator
    def _axiom_4(cls, v) -> Any:
        """Axiom 4: The asset must be created and owned by the 2-sig
        [Gnf Admin, payload.DeedValidator] multi account"""
        mtx = encoding.future_msgpack_decode(v.get("FirstDeedTransferMtx", None))
        txn = mtx.transaction
        DeedValidatorAddr = v.get("DeedValidatorAddr", None)
        settings = config.VanillaSettings(_env_file=dotenv.find_dotenv())
        client: AlgodClient = AlgodClient(
            settings.algo_api_secrets.algod_token.get_secret_value(),
            settings.public.algod_address,
        )
        gnf_admin_addr = config.GnfPublic().gnf_admin_addr
        v_multi = MultisigAccount(
            version=1,
            threshold=2,
            addresses=[gnf_admin_addr, DeedValidatorAddr],
        )
        ta_deed_idx = txn.dictify()["xaid"]
        try:
            created_assets = client.account_asset_info(
                address=v_multi.addr, asset_id=ta_deed_idx
            )
        except:
            raise ValueError(
                f"Axiom 4: The asset {ta_deed_idx} must be created and owned by the 2-sig "
                "[Gnf Admin, payload.DeedValidator] multi account. Not created"
            )
        if created_assets["asset-holding"]["amount"] == 0:
            raise ValueError(
                f"Axiom 4: The asset {ta_deed_idx} must be created and owned by the 2-sig "
                "[Gnf Admin, payload.DeedValidator] multi account. Created but not owned"
            )
        return v

    def _axiom_5(cls, v) -> Any:
        """Axiom 5: The 2-sig [Gnf Admin, TaDaemonAddr, TaOwnerAddr] account has opted in
        to the Deed and has enough funding (TaDeed Consideration Algos, publicly set by the Gnf)"""
        mtx = encoding.future_msgpack_decode(v.get("FirstDeedTransferMtx", None))
        txn = mtx.transaction
        TaDaemonAddr = v.get("TaDaemonAddr")
        TaOwnerAddr = v.get("TaOwnerAddr")
        settings = config.VanillaSettings(_env_file=dotenv.find_dotenv())
        client: AlgodClient = AlgodClient(
            settings.algo_api_secrets.algod_token.get_secret_value(),
            settings.public.algod_address,
        )
        gnf_admin_addr = config.GnfPublic().gnf_admin_addr
        ta_multi = MultisigAccount(
            version=1,
            threshold=2,
            addresses=[gnf_admin_addr, TaDaemonAddr, TaOwnerAddr],
        )
        ta_deed_idx = txn.dictify()["xaid"]
        try:
            client.account_asset_info(address=ta_multi.addr, asset_id=ta_deed_idx)
        except:
            raise ValueError(
                "Axiom 5: 2-sig [Gnf Admin, TaDaemonAddr, TaOwnerAddr must be opted in"
                f"to deed {ta_deed_idx}. It is not"
            )
        multi_algos = algo_utils.algos(ta_multi.addr)
        if multi_algos is None:
            raise ValueError(
                "Axiom 5: 2-sig [Gnf Admin, TaDaemonAddr, TaOwnerAddr must have at least"
                f"TaDeed Consideration Algos ({config.GnfPublic().ta_deed_consideration_algos}). Has none"
            )
        elif multi_algos < config.GnfPublic().ta_deed_consideration_algos:
            raise ValueError(
                "Axiom 5: 2-sig [Gnf Admin, TaDaemonAddr, TaOwnerAddr must have at least"
                f"TaDeed Consideration Algos ({config.GnfPublic().ta_deed_consideration_algos}). Has none"
            )
        return v

    @root_validator
    def _axiom_6(cls, v) -> Any:
        """Axiom 6: The 2-sig [Gnf Admin, TaDaemonAddr, TaOwnerAddr] must not own any assets
        (specifically because this is the FIRST tadeed and should initialize the multi."""
        TaDaemonAddr = v.get("TaDaemonAddr")
        TaOwnerAddr = v.get("TaOwnerAddr")
        settings = config.VanillaSettings(_env_file=dotenv.find_dotenv())
        client: AlgodClient = AlgodClient(
            settings.algo_api_secrets.algod_token.get_secret_value(),
            settings.public.algod_address,
        )
        gnf_admin_addr = config.GnfPublic().gnf_admin_addr
        ta_multi = MultisigAccount(
            version=1,
            threshold=2,
            addresses=[gnf_admin_addr, TaDaemonAddr, TaOwnerAddr],
        )
        opt_in_assets = client.account_info(address=ta_multi.addr)["assets"]
        owned = list(
            map(
                lambda x: x["asset-id"],
                list(filter(lambda x: x["amount"] != 0, opt_in_assets)),
            )
        )
        if len(owned) > 0:
            raise ValueError(
                "Axiom 6: The 2-sig [Gnf Admin, TaDaemonAddr, TaOwnerAddr] must not own"
                " any assets (specifically because this is the FIRST tadeed and should initialize"
                f"the multi. Owns: {owned}"
            )
        return v

    @root_validator
    def _axiom_7(cls, v) -> Any:
        """Axiom 7: The Mtx must be signed by the DeedValidatorAddr"""
        mtx = encoding.future_msgpack_decode(v.get("FirstDeedTransferMtx", None))
        DeedValidatorAddr = v.get("DeedValidatorAddr")
        try:
            api_utils.check_mtx_subsig(mtx, DeedValidatorAddr)
        except SchemaError as e:
            raise ValueError(
                f"Axiom 5: The Mtx must be signed by the DeedValidatorAddr {e}"
            )
        return v

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class TadeedAlgoTransfer_Maker:
    type_name = "tadeed.algo.transfer"
    version = "000"

    def __init__(
        self,
        first_deed_transfer_mtx: str,
        micro_lat: int,
        deed_validator_addr: str,
        ta_daemon_addr: str,
        ta_owner_addr: str,
        micro_lon: int,
    ):

        self.tuple = TadeedAlgoTransfer(
            FirstDeedTransferMtx=first_deed_transfer_mtx,
            MicroLat=micro_lat,
            DeedValidatorAddr=deed_validator_addr,
            TaDaemonAddr=ta_daemon_addr,
            TaOwnerAddr=ta_owner_addr,
            MicroLon=micro_lon,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: TadeedAlgoTransfer) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> TadeedAlgoTransfer:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> TadeedAlgoTransfer:
        d2 = dict(d)
        if "FirstDeedTransferMtx" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FirstDeedTransferMtx")
        if "MicroLat" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MicroLat")
        if "DeedValidatorAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing DeedValidatorAddr")
        if "TaDaemonAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaDaemonAddr")
        if "TaOwnerAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaOwnerAddr")
        if "MicroLon" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MicroLon")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return TadeedAlgoTransfer(
            FirstDeedTransferMtx=d2["FirstDeedTransferMtx"],
            MicroLat=d2["MicroLat"],
            DeedValidatorAddr=d2["DeedValidatorAddr"],
            TaDaemonAddr=d2["TaDaemonAddr"],
            TaOwnerAddr=d2["TaOwnerAddr"],
            MicroLon=d2["MicroLon"],
            TypeName=d2["TypeName"],
            Version="000",
        )
