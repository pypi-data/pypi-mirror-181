from fastapi import FastAPI
from fastapi import HTTPException

from gnf.dev_utils.dev_validator import DevValidator
from gnf.schemata import TerminalassetCertifyHack
from gnf.utils import RestfulResponse


app = FastAPI()

validator = DevValidator()


@app.post("/terminalasset-certification/")
async def terminalasset_certify_hack_received(payload: TerminalassetCertifyHack):
    r = validator.terminalasset_certify_hack_received(payload)
    return r
