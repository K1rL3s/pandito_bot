from core.ids import TaskId, UserId
from core.services.roles import RolesService
from database.repos.logs import LogsRepo
from database.repos.tasks import TasksRepo
from database.repos.users import UsersRepo


class TasksService:
    def __init__(
        self,
        tasks_repo: TasksRepo,
        users_repo: UsersRepo,
        logs_repo: LogsRepo,
        roles_service: RolesService,
    ) -> None:
        self.tasks_repo = tasks_repo
        self.users_repo = users_repo
        self.logs_repo = logs_repo
        self.roles_service = roles_service

    async def create(
        self,
        title: str,
        description: str,
        reward: int,
        end_phrase: str,
        creator_id: UserId,
    ) -> TaskId:
        await self.roles_service.is_stager(creator_id)
        task = await self.tasks_repo.create(title, description, reward, end_phrase)
        return task.id

    async def delete(self, task_id: TaskId, master_id: UserId) -> None:
        await self.roles_service.is_stager(master_id)
        await self.tasks_repo.delete(task_id)
