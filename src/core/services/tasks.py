from database.repos.logs import LogsRepo
from database.repos.tasks import TasksRepo
from database.repos.users import UsersRepo


class TasksService:
    def __init__(
        self,
        tasks_repo: TasksRepo,
        users_repo: UsersRepo,
        logs_repo: LogsRepo,
    ) -> None:
        self.tasks_repo = tasks_repo
        self.users_repo = users_repo
        self.logs_repo = logs_repo
