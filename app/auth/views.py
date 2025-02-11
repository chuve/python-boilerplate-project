from pydantic import BaseModel, EmailStr, Field


class SignUpViaEmailPassword(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class SignInViaEmailPassword(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenPayload(BaseModel):
    refresh_token: str


class TokensResponse(BaseModel):
    access_token: str
    refresh_token: str
