from asyncpg import Pool


class LoggingDB:
    def __init__(self, db_pool: Pool) -> None:
        self.db_pool = db_pool

    async def log_action(self, user_id: int, description: str):
        async with self.db_pool.acquire() as conn:
            sql = """
            INSERT INTO logs (user_id, description) 
            VALUES ($1, $2)
            RETURNING id;
            """
            return await conn.fetchval(sql, user_id, description)

    async def get_user_logs(self, user_id: int):
        async with self.db_pool.acquire() as conn:
            sql = """
            SELECT * FROM logs 
            WHERE user_id = $1;
            """
            return await conn.fetch(sql, user_id)
