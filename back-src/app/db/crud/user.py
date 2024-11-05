from datetime import datetime

from app.db.models.user import User, UserInfoUpdate, UserRegister
from pydantic import EmailStr
from sqlmodel import Session, select


def get_user_by_email(*, session: Session, email: EmailStr):
    statement = select(User).where(User.email == email)
    res = session.exec(statement).first()
    return res


def create_user(*, session: Session, new_user: UserRegister):
    db_user = User(
        email=new_user.email,
        username="YY",
        password=new_user.password,
        create_time=new_user.create_time,
    )
    session.add(db_user)
    session.commit()


def authenticate_user(*, session: Session, email: EmailStr, password: str):
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if password != db_user.password:
        return None
    return db_user


def update_user_info(*, session: Session, new_user_info: UserInfoUpdate):
    pass
