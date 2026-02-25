"""Wristband auth client instances for the demo application."""

import os

from wristband.m2m_auth import AsyncWristbandM2MAuthClient, WristbandM2MAuthClient, WristbandM2MAuthConfig
from wristband.python_jwt import WristbandJwtValidatorConfig, create_wristband_jwt_validator

__all__ = ["async_wristband_m2m_auth", "sync_wristband_m2m_auth", "wristband_jwt_validator"]

# WRISTBAND_TOUCHPOINT - Configure and instantiate the sync and async M2M auth clients.
# Both clients share the same config and handle token acquisition, caching, and refresh.
_m2m_config = WristbandM2MAuthConfig(
    client_id=os.getenv("CLIENT_ID", ""),
    client_secret=os.getenv("CLIENT_SECRET", ""),
    wristband_application_vanity_domain=os.getenv("APPLICATION_VANITY_DOMAIN", ""),
)
sync_wristband_m2m_auth = WristbandM2MAuthClient(_m2m_config)
async_wristband_m2m_auth = AsyncWristbandM2MAuthClient(_m2m_config)

# WRISTBAND_TOUCHPOINT - Initialize the JWT validator with the Wristband application vanity domain.
# The validator fetches the public JWKS from Wristband to verify token signatures.
wristband_jwt_validator = create_wristband_jwt_validator(
    WristbandJwtValidatorConfig(
        wristband_application_vanity_domain=os.getenv("APPLICATION_VANITY_DOMAIN", ""),
    )
)
