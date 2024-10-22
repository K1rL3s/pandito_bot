from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models.base import AlchemyBaseModel


MAX_TG_NAME_LENGTH = 36


# Исхожу из того, что purchases - это покупки, которые СДЕЛАЛ пользователь
# (пока без корзины?)


class Purchases(AlchemyBaseModel):
    __tablename__ = "purchases"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        primary_key=True,
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        primary_key=True,
    )
    amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
