"""
A FastAPI app for the Minecraft API.

This app will have a /status endpoint which will return 200 if the server is alive.
It will also have a /deploy endpoint which will start the server if it is not already running.
It will have a /destroy endpoint which will stop the server if it is running.

The deploy and destroy endpoints will be responsible for creating a JSON message to post
to a AWS Step Function with a single variable: "command" which will be either "deploy" or "destroy".
The Step Function will then be responsible for starting and stopping the server.
"""


import json
import os
from dataclasses import dataclass, field
from typing import List, Literal, Optional, TypedDict

import boto3
from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

try:
    from mypy_boto3_stepfunctions.client import SFNClient
    from mypy_boto3_stepfunctions.type_defs import StartExecutionOutputTypeDef
except ImportError:
    print("Warning: boto3-stubs[stepfunctions] not installed")


ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "dev")
DEV_PORT: int = int(os.environ.get("PORT", "8000"))
STATE_MACHINE_ARN: str = os.environ.get("DEPLOY_SERVER_STEP_FUNCTIONS_STATE_MACHINE_ARN")
ROUTER = APIRouter()


class ProvisionMinecraftServerPayload(TypedDict):
    """Input format supported by the state machine that provisions/destroys the Minecraft server."""

    command: Literal["create", "destroy"]


def trigger_state_machine(payload: ProvisionMinecraftServerPayload) -> JSONResponse:
    """Send command to state machine.

    Parameters
    ----------
    data : dict
        A dictionary with a single key "command" which will be either "deploy" or "destroy".

    Returns
    -------
    JSONResponse
        A JSON response with a status code of 200 if the state machine was triggered successfully.
        A JSON response with a status code of 500 if the state machine was not triggered successfully.
    """
    sfn_client: SFNClient = boto3.client("stepfunctions")
    start_exec: StartExecutionOutputTypeDef = sfn_client.start_execution(
        stateMachineArn=STATE_MACHINE_ARN,
        input=json.dumps(payload),
    )
    if start_exec["ResponseMetadata"]["HTTPStatusCode"] != 200:
        return JSONResponse(content="Failure!", status_code=500)

    # get status of state machine
    # status = sfn_client.describe_execution(executionArn=start_exec["executionArn"])
    # return JSONResponse(content="Success! {status}", status_code=200)
    return JSONResponse(content="Success!", status_code=200)


@ROUTER.get("/status")
async def status(request: Request):
    """Return 200 to demonstrate that this REST API is reachable and can execute."""
    # return all of request scope as a dictionary
    return str(request.scope.get("aws", "AWS key not present"))


@ROUTER.get("/deploy")
async def deploy():
    """Start the server if it is not already running."""
    data = {"command": "deploy"}
    return trigger_state_machine(data)


@ROUTER.get("/destroy")
async def destroy():
    """Stop the server if it is running."""
    data = {"command": "destroy"}
    return trigger_state_machine(data)


@dataclass
class Config:
    """API settings that are defined at startup time."""

    allowed_cors_origins: List[str] = field(default_factory=lambda: [f"http://localhost:{DEV_PORT}"])


@dataclass
class Services:
    """
    Container for all ``Service``s used by the running application.

    The ``Service`` abstraction should be used for any code that
    makes calls over the network to services external to this API.
    """

    ...


def create_app(
    config: Optional[Config] = None,
) -> FastAPI:

    if not config:
        config = Config()

    app = FastAPI(
        title="Minecraft API",
        description="A FastAPI app for the Minecraft API.",
        version="0.0.1",
        docs_url="/",
        redoc_url=None,
        openapi_prefix=f"/{ENVIRONMENT}",
    )
    app.state.config: Config = config
    app.state.services = Services()

    # configure startup behavior: initialize services on startup
    @app.on_event("startup")
    async def on_startup():
        print(dict(os.environ))
        print("We're starting up!")

    # add routes
    app.include_router(ROUTER, tags=["Admin"])

    # add authorized CORS origins (add these origins to response headers to
    # enable frontends at these origins to receive requests from this API)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.allowed_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


def create_default_app() -> FastAPI:
    """
    Return an initialized FastAPI object using configuration from environment variables.

    This is a factory method that can be used by WSGI/ASGI runners like gunicorn and uvicorn.
    It is also useful for providing an application invokable by AWS Lambda.
    """
    config = Config()
    return create_app(config=config)


if __name__ == "__main__":
    import uvicorn

    config = Config()
    app = create_app(config=config)
    uvicorn.run(app, host="0.0.0.0", port=DEV_PORT)
