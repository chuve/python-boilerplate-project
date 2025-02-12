import logging
from datetime import datetime
from typing import cast
from uuid import UUID

from pydantic import BaseModel, EmailStr
from tortoise.contrib.pydantic import pydantic_model_creator  # type: ignore
from tortoise.exceptions import DoesNotExist, IntegrityError

from .models import User

logger = logging.getLogger(__name__)

UserPydantic = pydantic_model_creator(User, name="UserPydantic")


class UserDTO(BaseModel):
    """
    The pydantic_model_creator function dynamically generates a Pydantic model class at runtime.
    Since Python's type system operates at "edit time" (i.e., when you're writing code),
    it doesn't know about the dynamically generated class until the code is actually executed.
    This is why you can't directly use UserPydantic as a type hint.
    As a workaroud UserDTO is used as a static Pydantic model class for type hint.
    """

    id: UUID
    email: EmailStr
    first_name: str | None
    last_name: str | None
    password_hash: str
    created_at: datetime
    modified_at: datetime


class UserRepositoryException(Exception):
    pass


class UserRepository:
    _instance = None

    def __new__(cls) -> "UserRepository":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def create_user(self, email: str, password_hash: str) -> UserDTO:
        try:
            new_user = await User.create(email=email, password_hash=password_hash)
            user_pydantic_model = await UserPydantic.from_tortoise_orm(new_user)
            return cast(UserDTO, user_pydantic_model)
        except IntegrityError as ex:
            logger.error(ex)
            raise UserRepositoryException(f"User with email {email} already exist")

    async def get_user_by_email(self, email: str) -> UserDTO | None:
        try:
            user = await User.get(email=email)
            if user:
                user_pydantic_model = await UserPydantic.from_tortoise_orm(user)
                return cast(UserDTO, user_pydantic_model)
            return None
        except DoesNotExist as ex:
            logger.exception(ex)
            raise UserRepositoryException(f"User with email {email} doesn't exist")

    async def get_user_by_id(self, id: str) -> UserDTO | None:
        try:
            user = await User.get(id=id)
            if user:
                user_pydantic_model = await UserPydantic.from_tortoise_orm(user)
                return cast(UserDTO, user_pydantic_model)
            return None
        except DoesNotExist as ex:
            logger.exception(ex)
            raise UserRepositoryException(f"User with id {id} doesn't exist")


user_repository = UserRepository()
