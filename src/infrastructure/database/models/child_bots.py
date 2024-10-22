from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models.base import AlchemyBaseModel


TOKEN_LENGTH = 41


class ChildBotModel(AlchemyBaseModel):
    __tablename__ = "child_bots"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        unique=True,
        nullable=False,
    )
    token: Mapped[str] = mapped_column(
        String(TOKEN_LENGTH),
        nullable=False,
    )
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
