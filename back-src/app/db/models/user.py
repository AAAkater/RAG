from datetime import datetime
from enum import Enum

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    role: str
    username: str = Field(nullable=False)
    password: str = Field(nullable=False)
    create_time: datetime
    last_login_time: datetime
    status: "red" | "b"


class UserCreate(UserBase):
    pass


class UserRegister(UserBase):
    pass


class UserInfoUpdate(UserBase):
    pass


class UserPasswordUpdate(UserBase):
    pass


class User(UserBase, table=True):
    __tablename__ = "user"
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    nickname: str | None = Field(default=None, max_length=255)
    gender: str
    avatar: str
