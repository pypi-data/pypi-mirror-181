"""Type tadeed.algo.exchange, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal

import dotenv
from algosdk import encoding
from algosdk.future import transaction
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


class TadeedAlgoExchange(BaseModel):
    TaDaemonAddr: str  #
    TaOwnerAddr: str  #
    ValidatorAddr: str  #
    NewTaDeedIdx: int  #
    OldDeedTransferMtx: str  #
    TypeName: Literal["tadeed.algo.exchange"] = "tadeed.algo.exchange"
    Version: str = "000"

    _validator_ta_daemon_addr = predicate_validator(
        "TaDaemonAddr", property_format.is_algo_address_string_format
    )

    _validator_ta_owner_addr = predicate_validator(
        "TaOwnerAddr", property_format.is_algo_address_string_format
    )

    _validator_validator_addr = predicate_validator(
        "ValidatorAddr", property_format.is_algo_address_string_format
    )

    _validator_old_deed_transfer_mtx = predicate_validator(
        "OldDeedTransferMtx", property_format.is_algo_msg_pack_encoded
    )

    @root_validator(pre=True)
    def _axioms_4_and_5(cls, v) -> Any:
        """Axiom 1: Decoded OldDeedTransferMtx must have type MultisigTransaction.
        Axiom 2:  The OldDeedTransferMtx.txn must have type AssetConfigTxn"""
        mtx = encoding.future_msgpack_decode(v.get("OldDeedTransferMtx", None))
        if not isinstance(mtx, transaction.MultisigTransaction):
            raise ValueError(
                "Axiom 4: Decoded OldDeedTransferMtx must have type MultisigTransaction,"
                f" got {type(mtx)}"
            )
        txn = mtx.transaction
        if not isinstance(txn, transaction.AssetTransferTxn):
            raise ValueError(
                f"Axiom 2: The OldDeedTransferMtx.txn must have type AssetTransferTxn, got {type(txn)}"
            )
        return v

    @root_validator
    def _axiom_6(cls, v) -> Any:
        """Axiom 6 (Txn consistency check). Total must be 1, sender must be ta_multi, receiver
        must be GnfAdmin, asset must be a TaDeed"""
        mtx = encoding.future_msgpack_decode(v.get("OldDeedTransferMtx", None))
        txn = mtx.transaction
        settings = config.VanillaSettings(_env_file=dotenv.find_dotenv())
        client: AlgodClient = AlgodClient(
            settings.algo_api_secrets.algod_token.get_secret_value(),
            settings.public.algod_address,
        )
        gnf_admin_addr = config.GnfPublic().gnf_admin_addr
        TaDaemonAddr = v.get("TaDaemonAddr")
        TaOwnerAddr = v.get("TaOwnerAddr")
        ValidatorAddr = v.get("ValidatorAddr")
        ta_multi = MultisigAccount(
            version=1,
            threshold=2,
            addresses=[gnf_admin_addr, TaDaemonAddr, TaOwnerAddr],
        )
        v_multi = MultisigAccount(
            version=1, threshold=2, addresses=[gnf_admin_addr, ValidatorAddr]
        )
        if txn.sender != ta_multi.addr:
            raise ValueError(
                f"Axiom 6: Sender address ..{txn.sender[-6:]} must be ta_multi addr ..{ta_multi.addr[-6:]}"
            )
        od = txn.dictify()
        if txn.receiver != gnf_admin_addr:
            raise ValueError(
                f"Axiom 6: Receiver address ..{txn.receiver[-6:]} must be Gnf Adminaddr ..{gnf_admin_addr[-6:]}"
            )
        if txn.amount != 1:
            raise ValueError(f"Axiom 3: Transfer total must be 1, not {txn.amount}")
        ta_deed_idx = txn.index
        asset_dict = client.asset_info(ta_deed_idx)["params"]
        if (
            asset_dict["unit-name"] != "TADEED"
            or asset_dict["total"] != 1
            or asset_dict["manager"] != gnf_admin_addr
        ):
            raise ValueError(
                "Axiom 6 (Txn consistency check): asset must be a valid TaDeed!"
            )

        old_ta_deed_g_node_alias = asset_dict["name"]
        try:
            property_format.check_is_lrd_alias_format(old_ta_deed_g_node_alias)
        except SchemaError as e:
            raise ValueError(f"The asset name must have valid GNode format: {e}")
        universe = config.GnfPublic().universe
        try:
            property_format.check_world_alias_matches_universe(
                g_node_alias=old_ta_deed_g_node_alias, universe=universe
            )
        except:
            raise ValueError(
                f"Axiom 6: The asset name must be a potential GNodeAlias in a {universe} universe. {e}"
            )

        creator_addr = asset_dict["creator"]
        if creator_addr not in [v_multi.addr, gnf_admin_addr]:
            raise ValueError(
                f"Axiom 6: Creator must be Gnf Admin ..{gnf_admin_addr[-6:]} or "
                f"Validator Multi ..{v_multi.addr[-6:]}. Got {creator_addr[-6:]}"
            )

        gnf_graveyard_addr = config.GnfPublic().gnf_graveyard_addr
        manager_addr = asset_dict["manager"]
        if manager_addr not in [gnf_admin_addr, gnf_graveyard_addr]:
            raise ValueError(
                f"Axiom 6: Manager must be GnfAdmin ..{gnf_admin_addr[-6:]} or "
                f"GnfGraveyard ..{gnf_graveyard_addr[-6:]}. Got {manager_addr[-6:]}"
            )

        return v

    @root_validator
    def _axiom_7(cls, v: Any) -> Any:
        """Axiom 7 (TaDeed order): The asset index of the new deed must be greater than the
        asset index of the old deed"""
        mtx = encoding.future_msgpack_decode(v.get("OldDeedTransferMtx", None))
        NewTaDeedIdx = v.get("NewTaDeedIdx")
        txn = mtx.transaction
        old_ta_deed_idx = txn.index
        if old_ta_deed_idx > NewTaDeedIdx:
            raise ValueError(
                "Axiom 7 (TaDeed order):The asset index of the new deed must be greater than"
                " the asset index of the old deed "
            )
        return v

    @root_validator
    def _axiom_8(cls, v) -> Any:
        """Axiom 8 (Correctly signed): OldDeedTransferMtx must be signed by Gnf Admin, and the
        signature must match the txn."""
        mtx = encoding.future_msgpack_decode(v.get("OldDeedTransferMtx", None))

        gnf_admin_addr = config.GnfPublic().gnf_admin_addr
        try:
            api_utils.check_mtx_subsig(mtx, gnf_admin_addr)
        except SchemaError as e:
            raise ValueError(f"OldDeedTransferMtx must be signed by Gnf Admin: {e}")
        # TODO: check that the signature matches the txn
        return v

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())

    def __repr__(self):
        r = "ExchangeTadeedAlgo"
        r += f"\n       TypeName: {self.TypeName}"
        r += f"\n       TaOwnerAddr: {self.TaOwnerAddr}"
        r += f"\n       TaDaemonAddr: {self.TaDaemonAddr}"
        r += f"\n       ValidatorAddr: {self.TaDaemonAddr}"
        r += f"\n       NewDeedIdx={self.NewTaDeedIdx}"
        mtx = encoding.future_msgpack_decode(self.OldDeedTransferMtx)
        msig = mtx.multisig
        sender = msig.address()
        od = mtx.transaction.dictify()
        total = od["aamt"]
        ta_deed_idx = od["xaid"]
        receiver = encoding.encode_address(od["arcv"])
        r += "\n       OldDeedTransferMtx - encoding of a half-signed mtx for transferring the old deed back to Gnf admin"
        r += f"\n         - sender=..{sender[-6:]}"
        r += f"\n         - total={total}"
        r += f"\n         - receiver=..{receiver[-6:]}"
        r += f"\n         - ta_deed_idx={ta_deed_idx}"
        return r


class TadeedAlgoExchange_Maker:
    type_name = "tadeed.algo.exchange"
    version = "000"

    def __init__(
        self,
        ta_daemon_addr: str,
        ta_owner_addr: str,
        validator_addr: str,
        new_ta_deed_idx: int,
        old_deed_transfer_mtx: str,
    ):

        self.tuple = TadeedAlgoExchange(
            TaDaemonAddr=ta_daemon_addr,
            TaOwnerAddr=ta_owner_addr,
            ValidatorAddr=validator_addr,
            NewTaDeedIdx=new_ta_deed_idx,
            OldDeedTransferMtx=old_deed_transfer_mtx,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: TadeedAlgoExchange) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> TadeedAlgoExchange:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> TadeedAlgoExchange:
        d2 = dict(d)
        if "TaDaemonAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaDaemonAddr")
        if "TaOwnerAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaOwnerAddr")
        if "ValidatorAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing ValidatorAddr")
        if "NewTaDeedIdx" not in d2.keys():
            raise SchemaError(f"dict {d2} missing NewTaDeedIdx")
        if "OldDeedTransferMtx" not in d2.keys():
            raise SchemaError(f"dict {d2} missing OldDeedTransferMtx")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return TadeedAlgoExchange(
            TaDaemonAddr=d2["TaDaemonAddr"],
            TaOwnerAddr=d2["TaOwnerAddr"],
            ValidatorAddr=d2["ValidatorAddr"],
            NewTaDeedIdx=d2["NewTaDeedIdx"],
            OldDeedTransferMtx=d2["OldDeedTransferMtx"],
            TypeName=d2["TypeName"],
            Version="000",
        )
