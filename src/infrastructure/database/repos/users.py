from asyncpg import Pool

from infrastructure.database.repos.base import BaseAlchemyRepo


class UserAlchemyRepo(BaseAlchemyRepo):
    def __init__(self, db_pool: Pool) -> None:
        self.db_pool = db_pool

    async def create_user(self, tg: int, name: str, is_admin=False):
        async with self.db_pool.acquire() as conn:
            sql = """
            INSERT INTO users (tg, name, is_admin) 
            VALUES ($1, $2, $3)
            RETURNING id;
            """
            return await conn.fetchval(sql, tg, name, is_admin)

    async def get_user(self, tg: int):
        async with self.db_pool.acquire() as conn:
            sql = "SELECT * FROM users WHERE tg = $1;"
            return await conn.fetchrow(sql, tg)

    async def get_all_users(self):
        async with self.db_pool.acquire() as conn:
            sql = "SELECT * FROM users"
            return await conn.fetch(sql)

    async def get_user_by_id(self, id: int):
        async with self.db_pool.acquire() as conn:
            sql = "SELECT * FROM users WHERE id = $1;"
            return await conn.fetchrow(sql, id)

    async def update_user_balance(self, id: int, amount: int, invoker: int):
        async with self.db_pool.acquire() as conn:
            invoker_user = await conn.fetchval(
                "SELECT id FROM users WHERE id = $1",
                invoker,
            )
            if not invoker_user:
                raise ValueError(
                    f"Invoker with id {invoker} does not exist in users table",
                )
            async with conn.transaction():
                # Обновляем баланс пользователя
                sql_update = """
                UPDATE users 
                SET balance = balance + $1, updated_at = NOW()
                WHERE id = $2 RETURNING balance;
                """
                new_balance = await conn.fetchval(sql_update, amount, id)

                # Добавляем запись в логи
                sql_insert_log = """
                INSERT INTO logs (user_id, description)
                VALUES ($1, $2);
                """
                await conn.execute(
                    sql_insert_log,
                    invoker,
                    f"Added money {amount} to user {id}",
                )
        return new_balance

    async def set_user_balance(self, id: int, amount: int, invoker: int):
        async with self.db_pool.acquire() as conn:
            sql = """
            UPDATE users 
            SET balance = $1, updated_at = NOW()
            WHERE id = $2 RETURNING balance;
            INSERT INTO logs (user_id, description)
            VALUES (user_id, 'Set money ' || $1 || ' to ' || $2 || ' user');
            """
            return await conn.fetchval(sql, amount, id, invoker)

    async def change_user_stage(self, id: int, stage: int):
        async with self.db_pool.acquire() as conn:
            sql = """
            UPDATE users 
            SET stage = $1, updated_at = NOW()
            WHERE id = $2 RETURNING stage;
            """
            return await conn.fetchval(sql, stage, id)

    async def is_user_admin(self, tg: int):
        async with self.db_pool.acquire() as conn:
            sql = """
            SELECT is_admin 
            FROM users 
            WHERE tg = $1;
            """
            return await conn.fetchval(sql, tg)

    async def get_user_purchases(self, user_id: int):
        async with self.db_pool.acquire() as conn:
            sql = """
            SELECT 
                p.id AS product_id,
                p.name AS product_name,
                p.description AS product_description,
                p.price AS product_price,
                pu.quantity AS quantity_purchased,
                pu.created_at AS purchase_date
            FROM 
                purchases pu
            JOIN 
                products p ON pu.product_id = p.id
            WHERE 
                pu.user_id = (SELECT id FROM users WHERE id = $1);
            """
            return await conn.fetch(sql, user_id)

    async def clear_user_purchases(self, user_id: int):
        async with self.db_pool.acquire() as conn:
            sql = "DELETE FROM purchases WHERE user_id = $1;"
            await conn.execute(sql, user_id)

    async def transfer_funds(self, sender_id: int, receiver_id: int, amount: int):
        async with self.db_pool.acquire() as conn:
            sql = "SELECT transfer_funds($1, $2, $3);"
            return await conn.fetchval(sql, sender_id, receiver_id, amount)
