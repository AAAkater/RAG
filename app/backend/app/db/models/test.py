from datetime import datetime

from sqlmodel import Field, SQLModel


class TestBase(SQLModel):
    name: str
    create_time: datetime


class Test(TestBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class TestUpdate(SQLModel):
    name: str | None = None
    create_time: datetime | None = None


class TestCreate(TestBase):
    pass
