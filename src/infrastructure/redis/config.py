import os
from dataclasses import dataclass


@dataclass
class RedisConfig:
    host: str
    port: int
    db: int
    password: str | None = None

    @property
    def url(self) -> str:
        return (
            "redis://"
            + (f"{self.password}@" if self.password else "")
            + f"{self.host}:{self.port}/{self.db}"
        )


def create_redis_config_from_env() -> RedisConfig | None:
    if "REDIS_HOST" not in os.environ:
        return None

    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", 6379))
    db = int(os.getenv("REDIS_DB", 0))
    password = os.getenv("REDIS_PASSWORD", None)

    return RedisConfig(host=host, port=port, db=db, password=password)
