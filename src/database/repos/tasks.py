from sqlalchemy import delete, func, select, update

from core.ids import TaskId, UserId
from database.models import TaskModel, UsersToTasksModel
from database.repos.base import BaseAlchemyRepo


class TasksRepo(BaseAlchemyRepo):
    async def get_by_id(self, task_id: TaskId) -> TaskModel | None:
        query = select(TaskModel).where(TaskModel.id == task_id)
        return await self.session.scalar(query)

    async def get_all(self) -> list[TaskModel]:
        query = select(TaskModel).order_by(TaskModel.id.asc())
        return list(await self.session.scalars(query))

    async def create(
        self,
        text: str,
        reward: int,
        activation_limit: int,
    ) -> TaskModel:
        task = TaskModel(
            text=text,
            reward=reward,
            activation_limit=activation_limit,
        )
        self.session.add(task)
        await self.session.flush()
        return task

    async def delete(self, task_id: TaskId) -> None:
        query = delete(TaskModel).where(TaskModel.id == task_id)
        await self.session.execute(query)
        await self.session.flush()

    async def is_activation_available(
        self,
        task_id: TaskId,
        activation_limit: int | None = None,
    ) -> bool:
        activations = await self.total_activations(task_id)

        if activation_limit is None:
            task = await self.get_by_id(task_id)
            activation_limit = task.activation_limit

        return activations < activation_limit

    async def total_activations(self, task_id: TaskId) -> int:
        query = select(
            func.count(UsersToTasksModel.created_at),
        ).where(
            UsersToTasksModel.task_id == task_id,
        )
        return await self.session.scalar(query)

    async def link_user_to_task(self, user_id: UserId, task_id: TaskId) -> None:
        user_to_task = UsersToTasksModel(user_id=user_id, task_id=task_id)
        self.session.add(user_to_task)
        await self.session.flush()

    async def set_task_status(
        self,
        user_id: UserId,
        task_id: TaskId,
        status: bool,
    ) -> None:
        query = (
            update(UsersToTasksModel)
            .where(
                UsersToTasksModel.user_id == user_id,
                UsersToTasksModel.task_id == task_id,
            )
            .values(status=status)
        )
        await self.session.execute(query)
        await self.session.flush()

    async def is_task_claimed(
        self,
        user_id: UserId,
        task_id: TaskId,
    ) -> bool:
        query = select(UsersToTasksModel).where(
            UsersToTasksModel.user_id == user_id,
            UsersToTasksModel.task_id == task_id,
        )
        relation = await self.session.scalar(query)
        return relation.status
