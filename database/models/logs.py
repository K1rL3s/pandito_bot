import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import BaseAlchemyModel, utc_now


class LogsModel(BaseAlchemyModel):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    description: Mapped[str] = mapped_column(String(4096), nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=utc_now,
        server_default=func.now(),
    )
