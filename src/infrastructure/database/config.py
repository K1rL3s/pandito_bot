import os
from dataclasses import dataclass


@dataclass
class DBConfig:
    driver: str
    host: str
    port: int
    user: str
    password: str
    name: str


def create_db_config_from_env() -> DBConfig:
    driver = os.getenv("DB_DRIVER", "postgresql+psycopg")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", 5432)
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "postgres")
    name = os.getenv("DB_NAME", "postgres")

    return DBConfig(
        driver=driver,
        host=host,
        port=port,
        user=user,
        password=password,
        name=name,
    )
