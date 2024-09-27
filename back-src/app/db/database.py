from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_NAME = "rag"

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:1234@localhost:3306/{DATABASE_NAME}"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


if __name__ == "__main__":
    # with engine.connect() as connection:
    #     result = connection.execute("show databases")
    #     print(result)

    pass
