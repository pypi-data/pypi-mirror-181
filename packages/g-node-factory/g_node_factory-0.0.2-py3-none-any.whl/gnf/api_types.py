""" List of all the types used"""
from typing import Dict
from typing import List

from gnf.schemata import BasegnodeCtnCreate_Maker
from gnf.schemata import BasegnodeGt_Maker
from gnf.schemata import BasegnodeMarketmakerCreate_Maker
from gnf.schemata import BasegnodeOtherCreate_Maker
from gnf.schemata import BasegnodesBroadcast_Maker
from gnf.schemata import BasegnodesGet_Maker
from gnf.schemata import BasegnodeTerminalassetCreate_Maker
from gnf.schemata import DebugTcReinitializeTime_Maker
from gnf.schemata import DiscoverycertAlgoCreate_Maker
from gnf.schemata import DiscoverycertAlgoTransfer_Maker
from gnf.schemata import HeartbeatA_Maker
from gnf.schemata import InitialTadeedAlgoCreate_Maker
from gnf.schemata import InitialTadeedAlgoOptin_Maker
from gnf.schemata import InitialTadeedAlgoTransfer_Maker
from gnf.schemata import NewTadeedAlgoOptin_Maker
from gnf.schemata import NewTadeedSend_Maker
from gnf.schemata import OldTadeedAlgoReturn_Maker
from gnf.schemata import PauseTime_Maker
from gnf.schemata import ResumeTime_Maker
from gnf.schemata import SlaEnter_Maker
from gnf.schemata import TadeedSpecsHack_Maker
from gnf.schemata import TatradingrightsAlgoCreate_Maker
from gnf.schemata import TavalidatorcertAlgoCreate_Maker
from gnf.schemata import TavalidatorcertAlgoTransfer_Maker
from gnf.schemata import TerminalassetCertifyHack_Maker


TypeMakerByName: Dict[str, HeartbeatA_Maker] = {}

type_makers: List[HeartbeatA_Maker] = [
    BasegnodeCtnCreate_Maker,
    BasegnodeGt_Maker,
    BasegnodeMarketmakerCreate_Maker,
    BasegnodeOtherCreate_Maker,
    BasegnodeTerminalassetCreate_Maker,
    BasegnodesBroadcast_Maker,
    BasegnodesGet_Maker,
    DebugTcReinitializeTime_Maker,
    DiscoverycertAlgoCreate_Maker,
    DiscoverycertAlgoTransfer_Maker,
    HeartbeatA_Maker,
    InitialTadeedAlgoCreate_Maker,
    InitialTadeedAlgoOptin_Maker,
    InitialTadeedAlgoTransfer_Maker,
    NewTadeedAlgoOptin_Maker,
    NewTadeedSend_Maker,
    OldTadeedAlgoReturn_Maker,
    PauseTime_Maker,
    ResumeTime_Maker,
    SlaEnter_Maker,
    TadeedSpecsHack_Maker,
    TatradingrightsAlgoCreate_Maker,
    TavalidatorcertAlgoCreate_Maker,
    TavalidatorcertAlgoTransfer_Maker,
    TerminalassetCertifyHack_Maker,
]


def version_by_type_name() -> List[str]:
    """
    Returns:
        Dict[str, str]: Keys are TypeNames, values are versions
    """

    v: Dict = {
        "basegnode.ctn.create": "000",
        "basegnode.gt": "000",
        "basegnode.marketmaker.create": "000",
        "basegnode.other.create": "000",
        "basegnode.terminalasset.create": "000",
        "basegnodes.broadcast": "000",
        "basegnodes.get": "000",
        "debug.tc.reinitialize.time": "000",
        "discoverycert.algo.create": "000",
        "discoverycert.algo.transfer": "000",
        "heartbeat.a": "000",
        "initial.tadeed.algo.create": "000",
        "initial.tadeed.algo.optin": "001",
        "initial.tadeed.algo.transfer": "000",
        "new.tadeed.algo.optin": "000",
        "new.tadeed.send": "000",
        "old.tadeed.algo.return": "000",
        "pause.time": "000",
        "resume.time": "000",
        "sla.enter": "000",
        "tadeed.specs.hack": "000",
        "tatradingrights.algo.create": "000",
        "tavalidatorcert.algo.create": "000",
        "tavalidatorcert.algo.transfer": "000",
        "terminalasset.certify.hack": "000",
    }

    return v


def status_by_versioned_type_name() -> List[str]:
    """
    Returns:
        Dict[str, str]: Keys are versioned TypeNames, values are type status
    """

    v: Dict = {
        "basegnode.ctn.create.000": "Pending",
        "basegnode.gt.000": "Pending",
        "basegnode.marketmaker.create.000": "Pending",
        "basegnode.other.create.000": "Pending",
        "basegnode.terminalasset.create.000": "Pending",
        "basegnodes.broadcast.000": "Pending",
        "basegnodes.get.000": "Pending",
        "debug.tc.reinitialize.time.000": "Pending",
        "discoverycert.algo.create.000": "Pending",
        "discoverycert.algo.transfer.000": "Pending",
        "heartbeat.a.000": "Pending",
        "initial.tadeed.algo.create.000": "Active",
        "initial.tadeed.algo.optin.001": "Pending",
        "initial.tadeed.algo.transfer.000": "Pending",
        "new.tadeed.algo.optin.000": "Pending",
        "new.tadeed.send.000": "Pending",
        "old.tadeed.algo.return.000": "Pending",
        "pause.time.000": "Pending",
        "resume.time.000": "Pending",
        "sla.enter.000": "Pending",
        "tadeed.specs.hack.000": "Pending",
        "tatradingrights.algo.create.000": "Pending",
        "tavalidatorcert.algo.create.000": "Active",
        "tavalidatorcert.algo.transfer.000": "Active",
        "terminalasset.certify.hack.000": "Pending",
    }

    return v
