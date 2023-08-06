"""Type optin.tadeed.algo, version 100"""
import json
from typing import Any
from typing import Dict
from typing import Literal

import dotenv
from algosdk import encoding
from algosdk.future.transaction import SignedTransaction
from algosdk.v2client.algod import AlgodClient
from pydantic import BaseModel
from pydantic import root_validator

import gnf.algo_utils as algo_utils
import gnf.api_utils as api_utils
import gnf.config as config
import gnf.property_format as property_format
from gnf.errors import SchemaError
from gnf.property_format import predicate_validator


class OptinTadeedAlgo(BaseModel):
    TaDaemonAddr: str  #
    NewDeedIdx: int  #
    ValidatorAddr: str  #
    SignedTaDeedCreationTxn: str  #
    TypeName: Literal["optin.tadeed.algo"] = "optin.tadeed.algo"
    Version: str = "100"

    _validator_ta_daemon_addr = predicate_validator(
        "TaDaemonAddr", property_format.is_algo_address_string_format
    )

    _validator_validator_addr = predicate_validator(
        "ValidatorAddr", property_format.is_algo_address_string_format
    )

    _validator_signed_ta_deed_creation_txn = predicate_validator(
        "SignedTaDeedCreationTxn", property_format.is_algo_msg_pack_encoded
    )

    @root_validator(pre=True)
    def _axiom_1(cls, v) -> Any:
        """Axiom 1 (AssetConfigTransaction) Decoded SignedTaDeedCreationTxn must have type SignedTransaction"""
        SignedTaDeedCreationTxn = v.get("SignedTaDeedCreationTxn", None)
        if not property_format.is_algo_msg_pack_encoded(SignedTaDeedCreationTxn):
            raise ValueError(
                f"SignedTaDeedCreationTxn: is_algo_msg_pack_encoded fails for [{SignedTaDeedCreationTxn}]"
            )
        txn = encoding.future_msgpack_decode(SignedTaDeedCreationTxn)
        if not isinstance(txn, SignedTaDeedCreationTxn):
            raise ValueError(
                "Axiom 1 (AssetConfigTransaction)"
                "Decoded SignedTaDeedCreationTxn must have type SignedTransaction"
                f", got {type(txn)}"
            )
        return v

    @root_validator
    def _axiom_2(cls, v) -> Any:
        """Axiom 2 (Valid TaDeed): NewDeedIdx is an active TaDeed created and owned by GnfAdminAccount"""
        NewDeedIdx = v.get("NewDeedIdx", None)
        settings = config.VanillaSettings(_env_file=dotenv.find_dotenv())
        client: AlgodClient = AlgodClient(
            settings.algo_api_secrets.algod_token.get_secret_value(),
            settings.public.algod_address,
        )
        gnf_admin_addr = config.GnfPublic().gnf_admin_addr
        try:
            gnf_new_deed_info = client.account_asset_info(
                address=gnf_admin_addr, asset_id=NewDeedIdx
            )
        except:
            raise ValueError("Axiom 2: OptIn asset must be created by GnfAdminAccount!")
        if (
            gnf_new_deed_info["created-asset"]["unit-name"] != "TADEED"
            or gnf_new_deed_info["created-asset"]["total"] != 1
            or gnf_new_deed_info["created-asset"]["manager"] != gnf_admin_addr
        ):
            raise ValueError(
                "Axiom 2 (Valid TaDeed): Optin asset must be a valid TaDeed!"
            )
        ta_deed_g_node_alias = gnf_new_deed_info["created-asset"]["name"]
        try:
            property_format.check_is_lrd_alias_format(ta_deed_g_node_alias)
        except SchemaError as e:
            raise ValueError(f"Axiom 6: Optin asset must be a valid TaDeed! {e}")
        universe = config.GnfPublic().universe
        try:
            property_format.check_world_alias_matches_universe(
                g_node_alias=ta_deed_g_node_alias, universe=universe
            )
        except:
            raise ValueError(
                f"Axiom 2(Valid TaDeed). The asset not a valid TaDeed! asset name must be a potential GNodeAlias in a {universe} universe. {e}"
            )
        if gnf_new_deed_info["asset-holding"]["amount"] != 1:
            raise ValueError(
                "Axiom 2(Valid TaDeed): Optin asset must be owned by GnfAdminAccount!"
            )

        return v

    def _axiom_3(cls, v) -> Any:
        """Axiom 3 (Old TaDeed check)  TaDaemonAddr owns exactly 1 TaDeed. The creator
        of this old TaDeed is either the GnfAdminAccount or  the ValidatorMulti 2-sig
        [GnfAdminAccount, ValidatorAddr]. The asset index of the old TaDeed is
        less than the asset index of the new TaDeed. Finally, if the creator of the
        old TaDeed is the GnfAdminAccount, then the TaDaemonAddr is opted into (but
        does not own) exactly one TaDeed created by the ValidatorMulti account and
        owned by the GnfAdminAccount.
        """
        NewDeedIdx = v.get("NewDeedIdx", None)
        TaDaemonAddr = v.get("TaDaemonAddr", None)
        ValidatorAddr = v.get("ValidatorAddr", None)

        gnf_admin_addr = config.GnfPublic().gnf_admin_addr
        v_multi = algo_utils.Multisig(
            version=1, threshold=2, addresses=[gnf_admin_addr, ValidatorAddr]
        )
        # TODO: implement!
        return v

    @root_validator
    def _axiom_4(cls, v) -> Any:
        """Axiom 4 (Correctly Signed) SignedTaDeedCreationTxn must be signed by Gnf Admin, and the signature
        must match the txn."""
        mtx = encoding.future_msgpack_decode(v.get("SignedTaDeedCreationTxn", None))
        gnf_admin_addr = config.GnfPublic().gnf_admin_addr
        # try:
        #     api_utils.check_mtx_subsig(mtx, gnf_admin_addr)
        # except SchemaError as e:
        #     raise ValueError(
        #         f"Axiom 8 (Correctly Signed): NewDeedOptInMtx must be signed by Gnf Admin: {e}"
        #     )
        # TODO: check that the signature matches the txn
        return v

    def as_dict(self) -> Dict:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class OptinTadeedAlgo_Maker:
    type_name = "optin.tadeed.algo"
    version = "100"

    def __init__(
        self,
        ta_daemon_addr: str,
        new_deed_idx: int,
        validator_addr: str,
        signed_ta_deed_creation_txn: str,
    ):

        self.tuple = OptinTadeedAlgo(
            TaDaemonAddr=ta_daemon_addr,
            NewDeedIdx=new_deed_idx,
            ValidatorAddr=validator_addr,
            SignedTaDeedCreationTxn=signed_ta_deed_creation_txn,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: OptinTadeedAlgo) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> OptinTadeedAlgo:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict) -> OptinTadeedAlgo:
        d2 = dict(d)
        if "TaDaemonAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TaDaemonAddr")
        if "NewDeedIdx" not in d2.keys():
            raise SchemaError(f"dict {d2} missing NewDeedIdx")
        if "ValidatorAddr" not in d2.keys():
            raise SchemaError(f"dict {d2} missing ValidatorAddr")
        if "SignedTaDeedCreationTxn" not in d2.keys():
            raise SchemaError(f"dict {d2} missing SignedTaDeedCreationTxn")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return OptinTadeedAlgo(
            TaDaemonAddr=d2["TaDaemonAddr"],
            NewDeedIdx=d2["NewDeedIdx"],
            ValidatorAddr=d2["ValidatorAddr"],
            SignedTaDeedCreationTxn=d2["SignedTaDeedCreationTxn"],
            TypeName=d2["TypeName"],
            Version="100",
        )
