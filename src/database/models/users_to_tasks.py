from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.ids import TaskId, UserId
from database.models import TaskModel, UserModel
from database.models._mixins import CreatedAtMixin, UpdatedAtMixin
from database.models.base import BaseAlchemyModel


class UsersToTasksModel(CreatedAtMixin, UpdatedAtMixin, BaseAlchemyModel):
    __tablename__ = "users_to_tasks"

    user_id: Mapped[UserId] = mapped_column(ForeignKey("users.id"), primary_key=True)
    task_id: Mapped[TaskId] = mapped_column(ForeignKey("tasks.id"), primary_key=True)

    # False - не выполнено, True - выполнено
    status: Mapped[bool] = mapped_column(Boolean, nullable=False)

    user: Mapped[UserModel] = relationship(
        "UserModel",
        cascade="all,delete",
    )
    task: Mapped[TaskModel] = relationship(
        "TaskModel",
        cascade="all,delete",
    )