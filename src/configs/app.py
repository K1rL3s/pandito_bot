from dataclasses import dataclass

from bots.father.config import TelegramConfig, create_telegram_config_from_env
from configs.server import create_server_config_from_env, ServerConfig
from infrastructure.database.config import DBConfig, create_db_config_from_env
from infrastructure.redis.config import RedisConfig, create_redis_config_from_env


@dataclass
class AppConfig:
    telegram: TelegramConfig
    server: ServerConfig
    db: DBConfig
    redis: RedisConfig | None = None


def create_app_config_from_env() -> AppConfig:
    telegram = create_telegram_config_from_env()
    db = create_db_config_from_env()
    redis = create_redis_config_from_env()
    server = create_server_config_from_env()
    return AppConfig(telegram=telegram, db=db, redis=redis, server=server)
