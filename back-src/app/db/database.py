from typing import Annotated, Generator

from app.core.config import settings
from app.db.database import engine
from fastapi import Depends
from sqlmodel import Session, create_engine

engine = create_engine(url=str(settings.SQLALCHEMY_DATABASE_URI), echo=True)


def get_db_session() -> Generator[Session, None, None]:
    with Session(bind=engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db_session)]
