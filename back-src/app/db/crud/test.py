from datetime import datetime

from app.db.database import engine
from app.db.models.test import Test, TestCreate, TestUpdate
from sqlmodel import Session, select


def update_test(test_id: int, new_test: TestUpdate):
    with Session(bind=engine) as session:
        db_test = session.get(Test, test_id)
        if not db_test:
            print("不存在")
            return
        test_data = new_test.model_dump(exclude_unset=True)
        db_test.sqlmodel_update(test_data)
        session.add(db_test)
        session.commit()


def del_test(test_id: int):
    with Session(bind=engine) as session:
        db_test = session.get(Test, test_id)
        if not db_test:
            print("不存在")
            return

        session.delete(db_test)
        session.commit()


def add_test(new_test: TestCreate):
    with Session(bind=engine) as session:
        db_test = Test.model_validate(new_test)
        session.add(db_test)
        session.commit()
        session.refresh(db_test)
    # return db_test


def create_test(new_test: TestCreate):
    with Session(bind=engine) as session:
        db_test = Test.model_validate(new_test)
        session.add(db_test)
        session.commit()


if __name__ == "__main__":

    # create_test(new_test=TestCreate(name="123", create_time=datetime.now()))
    # update_test(2, TestUpdate(name="asdasd", create_time=datetime.now()))
    del_test(3)
