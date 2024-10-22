from typing import Any

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from configs.database import DBConfig


POOL_SIZE = 5
MAX_POOL_OVERFLOW = 10
CONNECTION_TIMEOUT = 10


sessionmaker_kwargs = {
    "autoflush": False,
    "future": True,
    "expire_on_commit": False,
}


async def init_database(
    db_settings: DBConfig,
    **kwargs: Any,
) -> async_sessionmaker[AsyncSession]:
    engine = create_engine(db_settings)

    # Проверка подключения к базе данных
    async with engine.begin():
        pass

    return async_sessionmaker(bind=engine, **{**sessionmaker_kwargs, **kwargs})


def create_engine(settings: DBConfig) -> AsyncEngine:
    database_url = URL.create(
        drivername=settings.driver,
        username=settings.user,
        password=settings.password,
        host=settings.host,
        port=settings.port,
        database=settings.name,
    )
    return create_async_engine(
        database_url,
        pool_size=POOL_SIZE,
        max_overflow=MAX_POOL_OVERFLOW,
        connect_args={"timeout": CONNECTION_TIMEOUT},
    )
