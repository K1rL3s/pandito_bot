import random
import string

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.ids import TaskId
from database.models._mixins import CreatedAtMixin
from database.models.base import BaseAlchemyModel

TASK_ID_LEN = 8


def task_id_generator() -> TaskId:
    return "".join(random.choices(string.ascii_letters + string.digits, k=TASK_ID_LEN))


class TaskModel(CreatedAtMixin, BaseAlchemyModel):
    __tablename__ = "tasks"

    id: Mapped[TaskId] = mapped_column(
        String(length=TASK_ID_LEN),
        primary_key=True,
        default=task_id_generator,
    )
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    text: Mapped[str] = mapped_column(String(1024 * 2), nullable=False)
    reward: Mapped[int] = mapped_column(Integer, nullable=False)
    activation_limit: Mapped[int] = mapped_column(Integer, nullable=False)
