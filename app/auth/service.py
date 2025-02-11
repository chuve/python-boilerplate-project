import asyncio
import logging
from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError
from pydantic import BaseModel

from ..settings import settings
from .repository import UserRepository, UserRepositoryException

ph = PasswordHasher()
user_repository = UserRepository()


class AuthServiceException(Exception):
    pass


logger = logging.getLogger(__name__)


class JwtPayload(BaseModel):
    sub: str
    exp: datetime


class AuthService:
    _instance = None
    ALGORITHM = "HS256"
    access_token_expire_minutes = 30

    def __new__(
        cls, secret_key: str, access_token_expire_minutes: int
    ) -> "AuthService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, secret_key: str, access_token_expire_minutes: int) -> None:
        self.access_token_expire_minutes = access_token_expire_minutes
        self.secret_key = secret_key

    @staticmethod
    async def hash_password(password: str) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, ph.hash, password)

    @staticmethod
    async def verify_password(password_hash: str, password: str) -> bool:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, ph.verify, password_hash, password)

    def generate_token(self, user_id: UUID) -> str:
        payload = JwtPayload(
            sub=str(user_id),
            exp=datetime.now(timezone.utc)
            + timedelta(minutes=self.access_token_expire_minutes),
        )
        token = jwt.encode(  # type: ignore
            payload=payload.model_dump(),
            key=self.secret_key,
            algorithm=AuthService.ALGORITHM,
        )
        return token

    def validate_token(self, token: str) -> JwtPayload | None:
        try:
            payload = jwt.decode(  # type: ignore
                token, key=self.secret_key, algorithms=[AuthService.ALGORITHM]
            )
            if payload:
                return JwtPayload(**payload)
        except jwt.ExpiredSignatureError as ex:
            logger.exception(ex)
            raise AuthServiceException("Token has expired") from ex
        except jwt.InvalidTokenError as ex:
            logger.exception(ex)
            raise AuthServiceException("Token is invalid") from ex

    async def sign_up_via_email_password(self, email: str, password: str) -> str | None:
        try:
            password_hash = await self.hash_password(password)
            user = await user_repository.create_user(email, password_hash)
            if user:
                return self.generate_token(user_id=user.id)
        except UserRepositoryException as ex:
            logger.exception(ex)
            raise AuthServiceException(ex)

    async def sign_in_via_email_password(self, email: str, password: str) -> str | None:
        try:
            user = await user_repository.find_user_by_email(email)
            if user:
                if await self.verify_password(user.password_hash, password):
                    return self.generate_token(user_id=user.id)
        except (VerifyMismatchError, VerificationError, UserRepositoryException) as ex:
            logger.exception(ex)
            raise AuthServiceException(ex)


auth_service = AuthService(
    secret_key=settings.jwt_secret_key,
    access_token_expire_minutes=settings.access_token_expire_minutes,
)
