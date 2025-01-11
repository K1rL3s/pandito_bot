from sqlalchemy import BigInteger, Boolean, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.ids import UserId
from database.models._mixins import CreatedAtMixin, UpdatedAtMixin
from database.models.base import BaseAlchemyModel


class UserModel(CreatedAtMixin, UpdatedAtMixin, BaseAlchemyModel):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("student_id", postgresql_nulls_not_distinct=True),
    )

    id: Mapped[UserId] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    student_id: Mapped[str] = mapped_column(String(8), nullable=True, unique=True)
    group: Mapped[str] = mapped_column(String(10), nullable=True)
    balance: Mapped[int] = mapped_column(Integer, nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    role: Mapped[str] = mapped_column(String(64), default=None, nullable=True)

    qrcode_image_id: Mapped[str] = mapped_column(
        String(128),
        nullable=True,
        unique=True,
    )
