from sqlalchemy import select, update

from database.models import UserModel
from database.repos.base import BaseAlchemyRepo


class UsersRepo(BaseAlchemyRepo):
    async def create_user(
        self,
        tg_id: int,
        name: str,
        is_admin: bool = False,
    ) -> UserModel:
        user = UserModel(id=tg_id, name=name, is_admin=is_admin)
        self.session.add(user)
        await self.session.commit()
        return user

    async def get_user(self, tg_id: int) -> UserModel | None:
        query = select(UserModel).where(UserModel.id == tg_id)
        return await self.session.scalar(query)

    async def get_all_users(self) -> list[UserModel]:
        query = select(UserModel).order_by(UserModel.created_at.desc())
        return list(await self.session.scalars(query))

    async def set_balance(self, tg_id: int, new_balance: int) -> None:
        query = (
            update(UserModel).where(UserModel.id == tg_id).values(balance=new_balance)
        )
        await self.session.execute(query)
        await self.session.commit()

    async def change_stage(self, tg_id: int, stage: int) -> None:
        query = update(UserModel).where(UserModel.id == tg_id).values(stage=stage)
        await self.session.execute(query)
        await self.session.commit()

    async def is_admin(self, tg_id: int) -> bool:
        user = await self.get_user(tg_id)
        return user.is_admin if user else False
        # return user and user.is_admin
