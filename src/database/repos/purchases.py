from dataclasses import dataclass

from sqlalchemy import delete, select

from database.models import ProductModel, PurchaseModel
from database.repos.base import BaseAlchemyRepo


@dataclass
class PurchasesInfo:
    total_products: int
    total_purchases: int
    formated_info: str


class PurchasesRepo(BaseAlchemyRepo):
    async def create(self, tg_id: int, product_id: int, quantity: int) -> PurchaseModel:
        purchase = PurchaseModel(
            user_id=tg_id,
            product_id=product_id,
            quantity=quantity,
        )
        self.session.add(purchase)
        await self.session.flush()
        return purchase  # TODO проверить что появился айдишник

    async def get_user_purchases(
        self,
        tg_id: int,
    ) -> list[tuple[ProductModel, PurchaseModel]]:
        query = (
            select(ProductModel, PurchaseModel)
            .join(PurchaseModel, PurchaseModel.product_id == ProductModel.id)
            .where(PurchaseModel.user_id == tg_id)
        )
        return list(await self.session.execute(query))

    async def clear_purchases(self, tg_id: int) -> None:
        query = delete(PurchaseModel).where(PurchaseModel.user_id == tg_id)
        await self.session.execute(query)
        await self.session.flush()

    @staticmethod
    def format_purchases(
        purchases: list[tuple[ProductModel, PurchaseModel]],
    ) -> PurchasesInfo:
        total_products = len({i[0].id for i in purchases})
        total_purchases = sum(i[1].quantity for i in purchases)

        product_to_purchases: dict[tuple[int, str], int] = {}
        for product, purchase in purchases:
            if (product.id, product.name) not in product_to_purchases:
                product_to_purchases[(product.id, product.name)] = 0
            product_to_purchases[(product.id, product.name)] += purchase.quantity

        formated_purchases = "\n".join(
            [
                f"<b>{key[1]}</b> — <i>x{value}</i>"
                for key, value in sorted(
                    product_to_purchases.items(),
                    key=lambda x: x[0],
                )
            ],
        )

        return PurchasesInfo(total_products, total_purchases, formated_purchases)
