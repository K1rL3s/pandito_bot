from asyncpg import Pool, create_pool

from database.logs import LoggingDB
from database.products import ProductDB
from database.users import UserDB


class Database(LoggingDB, ProductDB, UserDB):  # TODO: Разделить
    def __init__(self, db_pool: Pool) -> None:
        super().__init__(db_pool)

    @classmethod
    async def init(cls, pg_url: str) -> "Database":
        db_pool = await create_pool(pg_url)
        self = cls(db_pool)
        return self
