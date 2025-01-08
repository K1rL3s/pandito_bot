from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.ids import ProductId
from database.models._mixins import CreatedAtMixin, UpdatedAtMixin
from database.models.base import BaseAlchemyModel
from database.models.purchases import PurchaseModel


class ProductModel(CreatedAtMixin, UpdatedAtMixin, BaseAlchemyModel):
    __tablename__ = "products"

    id: Mapped[ProductId] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(2048), nullable=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)

    purchases: Mapped[list[PurchaseModel]] = relationship(
        "PurchaseModel",
        cascade="delete, delete-orphan",
    )
