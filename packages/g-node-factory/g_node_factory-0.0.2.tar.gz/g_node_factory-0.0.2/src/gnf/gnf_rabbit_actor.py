import logging
import os
from typing import Optional

import django
from algosdk.future import transaction
from algosdk.v2client.algod import AlgodClient

import gnf.algo_utils as algo_utils
import gnf.config as config
import gnf.gnf_db as gnf_db
from gnf.algo_utils import BasicAccount
from gnf.data_classes import BaseGNode
from gnf.enums import CoreGNodeRole
from gnf.enums import GNodeStatus
from gnf.enums import RegistryGNodeRole
from gnf.errors import SchemaError


LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)

from gnf.schemata import BasegnodeTerminalassetCreate
from gnf.schemata import DiscoverycertAlgoTransfer
from gnf.schemata import HeartbeatA


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gnf.django_related.settings")
django.setup()
from gnf.django_related.models import BaseGNodeDb


class GnfRabbitActor:
    """Used for sending broadcast (pub/sub) updates about the status of GNodes"""

    def __init__(self, settings: config.GnfSettings):
        # super(GNodeFactoryBase, self).__init__(
        #     settings=settings,
        #     g_node_type_short_alias="gnf",
        # )
        self.settings = settings
        self.client: AlgodClient = AlgodClient(
            settings.algo_api_secrets.algod_token.get_secret_value(),
            settings.public.algod_address,
        )
        self.admin_account: BasicAccount = BasicAccount(
            settings.admin_acct_sk.get_secret_value()
        )
        algo_utils.verify_account_exists_and_funded(self.admin_account.addr)
        self.graveyard_account: BasicAccount = BasicAccount(
            settings.graveyard_acct_sk.get_secret_value()
        )
        algo_utils.verify_account_exists_and_funded(self.graveyard_account.addr)
        gnf_db.load_g_nodes_as_data_classes()
        LOGGER.info(f"Database GNodeFactory initialized")

    ########################
    # RabbitMq router gb
    ########################

    def route_direct_message(
        self,
        from_g_node_role_value: str,
        from_g_node_alias: str,
        payload: BasegnodeTerminalassetCreate,
    ):
        LOGGER.info(f"Got {payload} from {from_g_node_alias}")
        if from_g_node_role_value != RegistryGNodeRole.GNodeRegistry.value:
            raise Exception(f"GNodeFactory only listens to GNodeRegistries")
        if payload.TypeName == HeartbeatA.TypeName:
            self.sample_payload_received(payload)

    ##########################
    # Messages Received
    ##########################

    def sample_payload_received(self, payload: HeartbeatA):
        """Used for testing the rabbitmq actor base"""
        if not isinstance(payload, HeartbeatA):
            raise SchemaError(f"payload must be HeartbeatA, got {type(payload)}")
        LOGGER.info(f"just received HeartbeatA {payload}")

    def update_ctn_to_active(self, payload: DiscoverycertAlgoTransfer) -> BaseGNodeDb:
        """
        Payload will be DiscoverycertAlgoTransfer.

        """

        ctn = BaseGNodeDb.objects.filter(alias=payload.GNodeAlias)[0]
        if ctn.dc.role != CoreGNodeRole.ConductorTopologyNode:
            raise Exception(f"Expected Ctn, got {ctn.dc.role}!")
        ctn.status_value = GNodeStatus.Active.value
        ctn.save()
        LOGGER.info(f"Ctn is now Active: {ctn}")
        return ctn

    def transfer_discoverycert_algo_received(
        self, payload: DiscoverycertAlgoTransfer
    ) -> Optional[BaseGNode]:
        """
        TODO: ADD!
        """

        if not isinstance(payload, DiscoverycertAlgoTransfer):
            LOGGER.warning(
                f"payload must be type DiscoverycertAlgoTransfer, got {type(payload)}. Ignoring!"
            )
            return None

        # TODO: find discovery cert that was already created and send it to discoverer
        txn = transaction.AssetTransferTxn(
            sender=self.admin_account.addr,
            receiver=payload.DiscovererAddr,
            amt=1,
            index=50,
        )
        ctn = self.update_ctn_to_active(payload)
        return ctn.dc
