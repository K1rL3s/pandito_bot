from os import getenv


def build_db_url(user: str, password: str, host: str, port: str, db: str) -> str:
    return f"postgres://{user}:{password}@{host}:{port}/{db}?sslmode=disable"


DATABASE_URL = build_db_url(
    getenv("POSTGRES_USER"),
    getenv("POSTGRES_PASSWORD"),
    getenv("POSTGRES_HOST"),
    getenv("POSTGRES_PORT"),
    getenv("POSTGRES_DB"),
)
