"""FastAPI application entry point."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

# Load .env before any other app imports so env vars are available at module level
load_dotenv()

from auth import async_wristband_m2m_auth, sync_wristband_m2m_auth  # noqa: E402
from routes import router  # noqa: E402


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan handler.

    On startup: warms up both M2M auth clients by fetching an initial token
    so the cache is primed before the first real request arrives.

    On shutdown: cleanly closes both clients, stopping background refresh
    threads/tasks and closing HTTP connections.
    """
    # ---------------------------------------------------------------------------
    # Startup
    # ---------------------------------------------------------------------------

    try:
        sync_wristband_m2m_auth.get_token()
        print("[M2M AUTH] Sync client token cached successfully.")
    except Exception as ex:
        print(f"[M2M AUTH] Failed to retrieve initial sync M2M token: {ex}")

    try:
        await async_wristband_m2m_auth.get_token()
        print("[M2M AUTH] Async client token cached successfully.")
    except Exception as ex:
        print(f"[M2M AUTH] Failed to retrieve initial async M2M token: {ex}")

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=6001, reload=True)
