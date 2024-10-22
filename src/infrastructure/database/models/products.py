from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models.base import AlchemyBaseModel


NAME_LENGTH = 41
DESCRIPTION_LENGTH = 4096


class ProductModel(AlchemyBaseModel):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True,
        nullable=False,
    )
    bot_id: Mapped[int] = mapped_column(
        ForeignKey("child_bots.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(NAME_LENGTH),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(DESCRIPTION_LENGTH),
        nullable=False,
    )
