from datetime import datetime
from typing import Annotated, Generator

from app.core.config import settings
from app.db.models.test import Test, TestCreate
from app.db.models.user import User, UserRegister
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

engine = create_engine(
    url=str(settings.SQLALCHEMY_DATABASE_URI),
    # echo=True,
)


def get_db_session() -> Generator[Session, None, None]:
    with Session(bind=engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db_session)]

# def init_db(session:Session):


if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)
    with Session(bind=engine) as session:
        #     db_item = Test.model_validate(
        #         TestCreate,
        #         update={
        #             "name": "qweqwe",
        #             "create_time": int(time.time()),
        #         },
        #     )
        #     session.add(db_item)
        #     session.commit()
        #     session.refresh(db_item)

        db_user = User.model_validate(
            UserRegister,
            update={
                "email": "1318382761@qq.com",
                "username": "yyy",
                "password": "asdsadfasfas",
                "create_time": datetime.now(),
            },
        )

        session.add(db_user)
        session.commit()
