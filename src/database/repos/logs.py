from sqlalchemy import select

from database.models.logs import LogsModel
from database.repos.base import BaseAlchemyRepo


class LogsRepo(BaseAlchemyRepo):
    async def log_action(self, user_id: int, description: str) -> int:
        log = LogsModel(user_id=user_id, description=description)
        self.session.add(log)
        await self.session.flush()
        return log.id  # TODO проверить что айди есть

    async def get_user_logs(self, user_id: int) -> list[LogsModel]:
        query = (
            select(LogsModel)
            .where(LogsModel.user_id == user_id)
            .order_by(LogsModel.created_at.desc())
        )
        return list(await self.session.scalars(query))
