from fastapi import APIRouter, HTTPException

from .service import AuthServiceException, auth_service
from .views import (
    RefreshTokenPayload,
    SignInViaEmailPassword,
    SignUpViaEmailPassword,
    TokensResponse,
)

router = APIRouter(prefix="/auth", tags=["users"])


@router.post("/email-password/sign-up")
async def sign_up_via_email_password(
    payload: SignUpViaEmailPassword,
) -> TokensResponse | None:
    try:
        tokens = await auth_service.sign_up_via_email_password(
            payload.email, payload.password
        )
        if tokens:
            return TokensResponse(**tokens.model_dump())
    except AuthServiceException as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/email-password/sign-in")
async def sign_in_via_email_password(
    payload: SignInViaEmailPassword,
) -> TokensResponse | None:
    try:
        tokens = await auth_service.sign_in_via_email_password(
            payload.email, payload.password
        )
        if tokens:
            return TokensResponse(**tokens.model_dump())
    except AuthServiceException as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/refresh-access-token")
async def refresh_token(payload: RefreshTokenPayload) -> TokensResponse | None:
    try:
        tokens = await auth_service.refresh_access_token(
            refresh_token=payload.refresh_token
        )
        if tokens:
            return TokensResponse(**tokens.model_dump())
    except AuthServiceException as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/email-otp/sign-up")
async def sign_up_via_email_otp() -> None:
    pass


@router.post("/email-otp/sign-up")
async def sign_in_via_email_otp() -> None:
    pass
