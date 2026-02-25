"""API route definitions for the demo application."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from wristband.python_jwt import JWTPayload

from dependencies import require_jwt
from protected_api_client import get_protected_data_async, get_protected_data_sync

router = APIRouter()


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


# ---------------------------------------------------------------------------
# Sync routes (demonstrates WristbandM2MAuthClient)
# ---------------------------------------------------------------------------


@router.get("/api/sync/public/data")
def get_sync_public_data() -> JSONResponse:
    """
    Public endpoint (sync). Does not require an access token.

    Calls the protected API using the sync M2M auth client and returns its response.
    Demonstrates use of WristbandM2MAuthClient in a synchronous FastAPI route.
    """
    try:
        protected_message = get_protected_data_sync()
        return JSONResponse(content={
            "public_message": "Sync public API called protected API successfully!",
            "protected_message": protected_message,
            "timestamp": _now(),
        })
    except Exception as ex:
        return JSONResponse(status_code=500, content={"error": str(ex)})


@router.get("/api/sync/protected/data")
def get_sync_protected_data(jwt_payload: JWTPayload = Depends(require_jwt)) -> JSONResponse:
    """
    Protected endpoint (sync). Requires a valid M2M access token.

    The require_jwt dependency validates the Bearer token in the Authorization
    header via the Wristband JWKS endpoint before this handler is invoked.
    """
    return JSONResponse(content={"message": f"Hello from the sync protected API! User ID: {jwt_payload.sub}"})


# ---------------------------------------------------------------------------
# Async routes (demonstrates AsyncWristbandM2MAuthClient)
# ---------------------------------------------------------------------------


@router.get("/api/async/public/data")
async def get_async_public_data() -> JSONResponse:
    """
    Public endpoint (async). Does not require an access token.

    Calls the protected API using the async M2M auth client and returns its response.
    Demonstrates use of AsyncWristbandM2MAuthClient in an async FastAPI route.
    """
    try:
        protected_message = await get_protected_data_async()
        return JSONResponse(content={
            "public_message": "Async public API called protected API successfully!",
            "protected_message": protected_message,
            "timestamp": _now(),
        })
    except Exception as ex:
        return JSONResponse(status_code=500, content={"error": str(ex)})


@router.get("/api/async/protected/data")
async def get_async_protected_data(jwt_payload: JWTPayload = Depends(require_jwt)) -> JSONResponse:
    """
    Protected endpoint (async). Requires a valid M2M access token.

    The require_jwt dependency validates the Bearer token in the Authorization
    header via the Wristband JWKS endpoint before this handler is invoked.
    """
    return JSONResponse(content={"message": f"Hello from the async protected API! User ID: {jwt_payload.sub}"})
