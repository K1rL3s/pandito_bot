from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models.base import AlchemyBaseModel


MAX_TG_NAME_LENGTH = 36


class UserModel(AlchemyBaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        unique=True,
        nullable=False,
    )
    tg_username: Mapped[str | None] = mapped_column(
        String(MAX_TG_NAME_LENGTH),
        nullable=True,
    )
