from fastapi import APIRouter, HTTPException

from .service import AuthService, AuthServiceException
from .views import SignInViaEmailPassword, SignUpViaEmailPassword

router = APIRouter(prefix="/auth", tags=["users"])
auth_service = AuthService()


@router.post("/email-password/sign-up")
async def sign_up_via_email_password(payload: SignUpViaEmailPassword) -> None:
    try:
        return await auth_service.sign_up_via_email_password(
            payload.email, payload.password
        )
    except AuthServiceException as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/email-password/sign-in")
async def sign_in_via_email_password(payload: SignInViaEmailPassword) -> None:
    try:
        return await auth_service.sign_in_via_email_password(
            payload.email, payload.password
        )
    except AuthServiceException as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/email-otp/sign-up")
async def sign_up_via_email_otp() -> None:
    pass


@router.post("/email-otp/sign-up")
async def sign_in_via_email_otp() -> None:
    pass
