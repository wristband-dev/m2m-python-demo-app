"""FastAPI dependencies for protecting routes."""

import logging

from fastapi import HTTPException, Request, status
from wristband.python_jwt import JWTPayload

from auth import wristband_jwt_validator

logger = logging.getLogger(__name__)


def require_jwt(request: Request) -> JWTPayload:
    """FastAPI dependency that validates a Bearer token on protected routes.

    Extracts the Bearer token from the Authorization header, validates the
    signature, expiry, issuer, and algorithm against the Wristband JWKS endpoint,
    and returns the decoded JWT payload on success.

    Raises:
        HTTPException: 401 Unauthorized if the token is missing, invalid, or expired.
    """
    try:
        # WRISTBAND_TOUCHPOINT - Extract and validate the Bearer token from the request
        auth_header = request.headers.get("authorization")
        token = wristband_jwt_validator.extract_bearer_token(auth_header)
        result = wristband_jwt_validator.validate(token)

        if not result.is_valid or not result.payload:
            logger.debug(f"JWT validation failed: {result.error_message}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return result.payload

    except HTTPException:
        raise
    except Exception as e:
        logger.debug(f"JWT validation error: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
