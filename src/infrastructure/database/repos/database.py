from asyncpg import Pool, create_pool

from infrastructure.database.repos.logging import LoggingRepo
from infrastructure.database.repos.products import ProductsRepo
from infrastructure.database.repos.users import UserAlchemyRepo


class Database(LoggingRepo, ProductsRepo, UserAlchemyRepo):  # TODO: Разделить
    def __init__(self, db_pool: Pool) -> None:
        super().__init__(db_pool)

    @classmethod
    async def init(cls, pg_url: str) -> "Database":
        db_pool = await create_pool(pg_url)
        self = cls(db_pool)
        return self
