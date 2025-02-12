from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .auth.repository import UserDTO, UserRepositoryException, user_repository
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


async def current_user(
    user_id: Annotated[str, Depends(validate_token)],
) -> UserDTO | None:
    try:
        current_user = await user_repository.get_user_by_id(user_id)
        return current_user
    except UserRepositoryException:
        return None
