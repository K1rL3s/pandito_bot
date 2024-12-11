from sqlalchemy import BigInteger, Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models._mixins import CreatedAtMixin, UpdatedAtMixin
from database.models.base import BaseAlchemyModel
from database.models.logs import LogsModel
from database.models.purchases import PurchaseModel


class UserModel(CreatedAtMixin, UpdatedAtMixin, BaseAlchemyModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    balance: Mapped[int] = mapped_column(Integer, nullable=False)
    stage: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    can_pay: Mapped[bool] = mapped_column(Boolean, default=False)
    can_clear_purchases: Mapped[bool] = mapped_column(Boolean, default=False)

    purchases: Mapped[list[PurchaseModel]] = relationship(
        "PurchaseModel",
        cascade="delete, delete-orphan",
    )
    logs: Mapped[list[LogsModel]] = relationship(
        "LogsModel",
        cascade="delete, delete-orphan",
    )
