from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)


class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64,
    )


class UserLoginOut(UserBase):
    user_id: Optional[str]
    message: str = Field(default='Login successfully')


class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )
    birthday: Optional[date]


class UserRegister(User, UserLogin):
    ...
