from fastapi import APIRouter, HTTPException

from .service import AuthServiceException, auth_service
from .views import SignInViaEmailPassword, SignUpViaEmailPassword, Token

router = APIRouter(prefix="/auth", tags=["users"])


@router.post("/email-password/sign-up")
async def sign_up_via_email_password(payload: SignUpViaEmailPassword) -> Token | None:
    try:
        token = await auth_service.sign_up_via_email_password(
            payload.email, payload.password
        )
        if token:
            return Token(access_token=token)
    except AuthServiceException as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/email-password/sign-in")
async def sign_in_via_email_password(payload: SignInViaEmailPassword) -> Token | None:
    try:
        token = await auth_service.sign_in_via_email_password(
            payload.email, payload.password
        )
        if token:
            return Token(access_token=token)
    except AuthServiceException as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/email-otp/sign-up")
async def sign_up_via_email_otp() -> None:
    pass


@router.post("/email-otp/sign-up")
async def sign_in_via_email_otp() -> None:
    pass
