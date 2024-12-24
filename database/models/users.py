from sqlalchemy import BigInteger, Boolean, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.enums import RightsRole
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
    role: Mapped[str] = mapped_column(String(64), default=None, nullable=True)

    qrcode_image_id: Mapped[str] = mapped_column(
        String(128),
        nullable=True,
        unique=True,
    )

    purchases: Mapped[list[PurchaseModel]] = relationship(
        "PurchaseModel",
        cascade="delete, delete-orphan",
    )
    logs: Mapped[list[LogsModel]] = relationship(
        "LogsModel",
        cascade="delete, delete-orphan",
    )

    @hybrid_property
    def is_admin(self) -> bool:
        return self.role == RightsRole.ADMIN

    @hybrid_property
    def is_seller(self) -> bool:
        return self.role == RightsRole.SELLER
