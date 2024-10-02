from app.db.database import Base


class User(Base):
    __tablename__: str = "user"
