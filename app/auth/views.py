from pydantic import BaseModel, EmailStr, Field


class SignUpViaEmailPassword(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class SignInViaEmailPassword(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
