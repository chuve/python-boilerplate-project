import asyncio
import logging

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError

from .repository import UserRepository, UserRepositoryException

ph = PasswordHasher()
user_repository = UserRepository()


class AuthServiceException(Exception):
    pass


logger = logging.getLogger(__name__)


class AuthService:
    @staticmethod
    async def hash_password(password: str) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, ph.hash, password)

    @staticmethod
    async def verify_password(password_hash: str, password: str) -> bool:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, ph.verify, password_hash, password)

    async def sign_up_via_email_password(self, email: str, password: str) -> None:
        try:
            password_hash = await self.hash_password(password)
            user = await user_repository.create_user(email, password_hash)
            if user:
                # generate jwt token
                return {"token": "123"}  # type: ignore
        except UserRepositoryException as ex:
            logger.error(ex)
            raise AuthServiceException(ex)

    async def sign_in_via_email_password(self, email: str, password: str) -> None:
        try:
            user = await user_repository.find_user_by_email(email)
            if user:
                await self.verify_password(user.password_hash, password)
                # generate jwt token
                return {"token": "123"}  # type: ignore
        except (VerifyMismatchError, VerificationError, UserRepositoryException) as ex:
            logger.error(ex)
            raise AuthServiceException(ex)
