from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .auth.service import AuthServiceException, auth_service

security = HTTPBearer()


def validate_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str | None:
    token = credentials.credentials
    try:
        payload = auth_service.validate_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        return payload.sub
    except AuthServiceException as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(ex),
        )
