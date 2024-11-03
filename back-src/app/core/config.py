from pydantic import PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # POSTGRESQL
    POSTGRESQL_USER: str
    POSTGRESQL_PASSWORD: str
    POSTGRESQL_PROT: int = 5432
    POSTGRESQL_SERVER: str
    POSTGRESQL_DB: str

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRESQL_USER,
            password=self.POSTGRESQL_PASSWORD,
            port=self.POSTGRESQL_PROT,
            host=self.POSTGRESQL_SERVER,
            path=self.POSTGRESQL_DB,
        )

    # EMAIL
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USERNAME: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAIL_FROM_NAME: str | None = None

    # TODO: MILVUS settings


settings = Settings()


if __name__ == "__main__":

    url = settings.SQLALCHEMY_DATABASE_URI

    print(url)
