"""HTTP client functions for calling the protected APIs."""

import httpx

from auth import async_wristband_m2m_auth, sync_wristband_m2m_auth

_BASE_URL = "http://localhost:6001"


def get_protected_data_sync() -> str:
    """Call the sync protected API using the sync M2M auth client."""
    token = sync_wristband_m2m_auth.get_token()

    response = httpx.get(
        f"{_BASE_URL}/api/sync/protected/data",
        headers={"Authorization": f"Bearer {token}"},
    )

    if response.status_code == 401:
        sync_wristband_m2m_auth.clear_token()

    response.raise_for_status()
    return str(response.json().get("message", ""))


async def get_protected_data_async() -> str:
    """Call the async protected API using the async M2M auth client."""
    token = await async_wristband_m2m_auth.get_token()

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{_BASE_URL}/api/async/protected/data",
            headers={"Authorization": f"Bearer {token}"},
        )

    if response.status_code == 401:
        async_wristband_m2m_auth.clear_token()

    response.raise_for_status()
    return str(response.json().get("message", ""))
