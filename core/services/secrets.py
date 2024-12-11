from sqlalchemy.exc import IntegrityError

from core.exceptions import NotAdmin, SecretAlreadyExists, UserNotFound
from database.repos.logs import LogsRepo
from database.repos.secrets import SecretsRepo
from database.repos.users import UsersRepo


class SecretsService:
    def __init__(
        self, secrets_repo: SecretsRepo, users_repo: UsersRepo, logs_repo: LogsRepo,
    ) -> None:
        self.secrets_repo = secrets_repo
        self.users_repo = users_repo
        self.logs_repo = logs_repo

    async def reward_for_secret(self, user_id: int, phrase: str) -> int | None:
        user = await self.users_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)

        secret = await self.secrets_repo.get(phrase)
        if secret is None:
            return None

        if await self.secrets_repo.is_user_already_claimed_secret(user_id, secret.id):
            return None

        await self.secrets_repo.link_user_to_secret(user_id, secret.id)
        await self.users_repo.set_balance(user_id, user.balance + secret.reward)

        await self.logs_repo.log_action(
            user_id,
            f"Reward {secret.reward} coins for secret {secret.id} id",
        )

        return secret.reward

    async def create_secret(self, phrase: str, reward: int, creator_id: int) -> int:
        creator = await self.users_repo.get_by_id(creator_id)
        if creator is None:
            raise UserNotFound(creator_id)
        if not creator.is_admin:
            raise NotAdmin(creator_id)

        try:
            secret = await self.secrets_repo.create(phrase, reward)
        except IntegrityError:  # TODO убрать отсюда импорт ошибки алхимии?
            raise SecretAlreadyExists(phrase)

        return secret.id
