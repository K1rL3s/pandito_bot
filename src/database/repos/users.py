from sqlalchemy import delete, select, update

from database.models import UserModel
from database.models.purchases import PurchaseModel
from database.repos.base import BaseAlchemyRepo


class UsersRepo(BaseAlchemyRepo):
    async def create_user(self, tg_id: int, name: str, is_admin: bool = False) -> int:
        user = UserModel(id=tg_id, name=name, is_admin=is_admin)
        self.session.add(user)
        await self.session.commit()
        return tg_id

    async def get_user(self, tg_id: int) -> UserModel | None:
        query = select(UserModel).where(UserModel.id == tg_id)
        return await self.session.scalar(query)

    async def get_all_users(self) -> list[UserModel]:
        query = select(UserModel)
        return list(await self.session.scalars(query))

    # TODO: в сервис
    async def update_balance(self, tg_id: int, amount: int, invoker: int):
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

    # TODO: в сервис
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

    async def change_user_stage(self, tg_id: int, stage: int) -> None:
        query = update(UserModel).where(UserModel.id == tg_id).values(stage=stage)
        await self.session.execute(query)
        await self.session.commit()

    async def is_admin(self, tg_id: int) -> bool:
        user = await self.get_user(tg_id)
        return user.is_admin if user else False
        # return user and user.is_admin

    # TODO: в сервис? или в репу покупок
    async def get_user_purchases(self, tg_id: int):
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
            return await conn.fetch(sql, tg_id)

    # TODO: в сервис? или в репу покупок
    async def clear_purchases(self, tg_id: int):
        query = delete(PurchaseModel).where(PurchaseModel.user_id == tg_id)
        await self.session.execute(query)
        await self.session.commit()

    # TODO: в сервис
    async def transfer_funds(self, sender_id: int, receiver_id: int, amount: int):
        async with self.db_pool.acquire() as conn:
            sql = "SELECT transfer_funds($1, $2, $3);"
            return await conn.fetchval(sql, sender_id, receiver_id, amount)
