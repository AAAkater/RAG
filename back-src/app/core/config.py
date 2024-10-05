from functools import lru_cache

from pydantic import MySQLDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    class Config:
        env_file = "../../.env"

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
            host=self.MYSQL_SERVER,
            path=self.MYSQL_DB,
        )

    # TODO: MILVUS settings


@lru_cache
def get_settings():
    return Settings()


if __name__ == "__main__":

    setting = get_settings()
    url = setting.SQLALCHEMY_DATABASE_URI

    print(url)
