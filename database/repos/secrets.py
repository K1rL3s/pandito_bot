from sqlalchemy import delete, select

from database.models import SecretModel, UsersToSecretsModel
from database.repos.base import BaseAlchemyRepo


class SecretsRepo(BaseAlchemyRepo):
    async def get(self, phrase: str) -> SecretModel | None:
        query = select(SecretModel).where(SecretModel.phrase == phrase)
        return await self.session.scalar(query)

    async def get_all(self) -> list[SecretModel]:
        query = select(SecretModel).order_by(SecretModel.id.asc())
        return list(await self.session.scalars(query))

    async def create(self, phrase: str, reward: int) -> SecretModel:
        secret = SecretModel(phrase=phrase, reward=reward)
        self.session.add(secret)
        await self.session.flush()
        return secret

    async def delete(self, secret_id: int) -> None:
        query = delete(SecretModel).where(SecretModel.id == secret_id)
        await self.session.execute(query)
        await self.session.flush()

    async def link_user_to_secret(self, user_id: int, secret_id: int) -> None:
        user_to_secret = UsersToSecretsModel(user_id=user_id, secret_id=secret_id)
        self.session.add(user_to_secret)
        await self.session.flush()

    async def is_user_already_claimed_secret(
        self,
        user_id: int,
        secret_id: int,
    ) -> bool:
        query = select(UsersToSecretsModel).where(
            UsersToSecretsModel.user_id == user_id,
            UsersToSecretsModel.secret_id == secret_id,
        )
        return bool(await self.session.scalar(query))
