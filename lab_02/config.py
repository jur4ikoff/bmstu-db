from pydantic_settings import BaseSettings, SettingsConfigDict
import os

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

CREATE_SQL = script_dir + "/sql_create/create_tables.sql"
COPY_SQL = script_dir + "/sql_create/copy_tables.sql"
DROP_SQL = script_dir + "/sql_create/drop_tables.sql"
LIMITATION_SQL = script_dir + "/sql_create/limitations.sql"


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )


settings = Settings()


def get_db_url():
    return (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
