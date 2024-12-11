import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import BaseAlchemyModel, utc_now
from database.models.logs import LogsModel
from database.models.purchases import PurchaseModel


class UserModel(BaseAlchemyModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    balance: Mapped[int] = mapped_column(Integer, nullable=False)
    stage: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    can_pay: Mapped[bool] = mapped_column(Boolean, default=False)
    can_clear_purchases: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=utc_now,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
        server_default=func.now(),
        server_onupdate=func.now(),
    )

    purchases: Mapped[list[PurchaseModel]] = relationship(
        "PurchaseModel",
        cascade="delete-orphan, delete",
    )
    logs: Mapped[list[LogsModel]] = relationship(
        "LogsModel",
        cascade="delete-orphan, delete",
    )
