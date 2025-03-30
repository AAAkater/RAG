import uuid
from datetime import datetime

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    role: str = Field(default="user", nullable=False)
    last_login_time: datetime = Field(default=datetime.now(), nullable=False)
    status: str = Field(default="good", nullable=False)
    email: EmailStr = Field(
        unique=True,
        index=True,
        max_length=255,
    )
    username: str = Field(default="tooler", nullable=False)
    password: str = Field(
        nullable=False,
        min_length=6,
        max_length=40,
    )
    create_time: datetime


class UserRegister(SQLModel):
    email: EmailStr = Field(
        unique=True,
        index=True,
        max_length=255,
    )
    password: str = Field(
        nullable=False,
        min_length=6,
        max_length=40,
    )
    create_time: datetime


class UserInfoUpdate(UserBase):
    pass


class UserPasswordUpdate(UserBase):
    pass


class User(UserBase, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )
    nickname: str = Field(
        default="AAA",
        max_length=255,
        nullable=True,
    )
    avatar: str = Field(default="no", nullable=False)
