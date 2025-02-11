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
    type: str


class Tokens(BaseModel):
    access_token: str
    refresh_token: str


class AuthService:
    _instance = None
    ALGORITHM = "HS256"
    access_token_expire_minutes = 30
    refresh_token_expire_minutes = 60 * 24 * 7  # 7 days

    def __new__(
        cls,
        secret_key: str,
        refresh_secret_key: str,
        access_token_expire_minutes: int,
        refresh_token_expire_minutes: int,
    ) -> "AuthService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        secret_key: str,
        refresh_secret_key: str,
        access_token_expire_minutes: int,
        refresh_token_expire_minutes: int,
    ) -> None:
        self.access_secret_key = secret_key
        self.refresh_secret_key = refresh_secret_key
        self.refresh_token_expire_minutes = refresh_token_expire_minutes
        self.access_token_expire_minutes = access_token_expire_minutes

    @staticmethod
    async def hash_password(password: str) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, ph.hash, password)

    @staticmethod
    async def verify_password(password_hash: str, password: str) -> bool:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, ph.verify, password_hash, password)

    def _get_token_secret_key(self, type: str) -> str | None:
        if type == "access":
            secret_key = self.access_secret_key
        elif type == "refresh":
            secret_key = self.refresh_secret_key
        else:
            raise AuthServiceException("Unknown type of token")
        return secret_key

    def _get_token_expire_timedelta(self, type: str) -> timedelta | None:
        if type == "access":
            token_expire_timedelta = timedelta(minutes=self.access_token_expire_minutes)
        elif type == "refresh":
            token_expire_timedelta = timedelta(
                minutes=self.refresh_token_expire_minutes
            )
        else:
            raise AuthServiceException("Unknown type of token")
        return token_expire_timedelta

    def _generate_tokens(self, user_id: UUID) -> Tokens | None:
        access_token = self._generate_token(type="access", user_id=user_id)
        refresh_token = self._generate_token(type="refresh", user_id=user_id)
        if access_token and refresh_token:
            return Tokens(access_token=access_token, refresh_token=refresh_token)

    def _generate_token(self, type: str, user_id: UUID) -> str | None:
        expire_timedelta = self._get_token_expire_timedelta(type)
        secret_key = self._get_token_secret_key(type)
        if expire_timedelta and secret_key:
            payload = JwtPayload(
                sub=str(user_id),
                exp=datetime.now(timezone.utc) + expire_timedelta,
                type=type,
            )
            token = jwt.encode(  # type: ignore
                payload=payload.model_dump(),
                key=secret_key,
                algorithm=AuthService.ALGORITHM,
            )
            return token

    def validate_token(self, token: str) -> JwtPayload | None:
        try:
            payload = jwt.decode(  # type: ignore
                token, key=self.access_secret_key, algorithms=[AuthService.ALGORITHM]
            )
            if payload:
                return JwtPayload(**payload)
        except jwt.ExpiredSignatureError as ex:
            logger.exception(ex)
            raise AuthServiceException("Access token has expired")
        except jwt.InvalidTokenError as ex:
            logger.exception(ex)
            raise AuthServiceException("Access token is invalid")

    async def refresh_access_token(self, refresh_token: str) -> Tokens | None:
        try:
            payload = jwt.decode(  # type: ignore
                refresh_token,
                key=self.refresh_secret_key,
                algorithms=[AuthService.ALGORITHM],
            )
            if payload.get("type") != "refresh":
                raise AuthServiceException("Invalid token type")
            access_token = self._generate_token(
                type="access", user_id=payload.get("sub")
            )
            if access_token:
                return Tokens(access_token=access_token, refresh_token=refresh_token)
        except jwt.ExpiredSignatureError as ex:
            logger.exception(ex)
            raise AuthServiceException("Refresh token has expired")
        except jwt.InvalidTokenError as ex:
            logger.exception(ex)
            raise AuthServiceException("Refresh token is invalid")

    async def sign_up_via_email_password(
        self, email: str, password: str
    ) -> Tokens | None:
        try:
            password_hash = await self.hash_password(password)
            user = await user_repository.create_user(email, password_hash)
            if user:
                return self._generate_tokens(user.id)
        except UserRepositoryException as ex:
            logger.exception(ex)
            raise AuthServiceException(ex)

    async def sign_in_via_email_password(
        self, email: str, password: str
    ) -> Tokens | None:
        try:
            user = await user_repository.find_user_by_email(email)
            if user:
                if await self.verify_password(user.password_hash, password):
                    return self._generate_tokens(user.id)
        except (VerifyMismatchError, VerificationError, UserRepositoryException) as ex:
            logger.exception(ex)
            raise AuthServiceException(ex)


auth_service = AuthService(
    secret_key=settings.jwt_secret_key,
    refresh_secret_key=settings.jwt_refresh_secret_key,
    access_token_expire_minutes=settings.access_token_expire_minutes,
    refresh_token_expire_minutes=settings.refresh_token_expire_minutes,
)
