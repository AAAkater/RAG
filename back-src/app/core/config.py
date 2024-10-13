from pydantic import MySQLDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # class Config:
    #     env_file = ""

    # MYSQL
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_PROT: int
    MYSQL_SERVER: str
    MYSQL_DB: str

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> MySQLDsn:
        return MultiHostUrl.build(
            scheme="mysql+pymysql",
            username=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            port=self.MYSQL_PROT,
            host=self.MYSQL_SERVER,
            path=self.MYSQL_DB,
        )

    # TODO: MILVUS settings


settings = Settings()


if __name__ == "__main__":

    url = settings.SQLALCHEMY_DATABASE_URI

    print(url)
