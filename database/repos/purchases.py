from sqlalchemy import delete, select

from database.models import ProductModel, PurchaseModel
from database.repos.base import BaseAlchemyRepo


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
        return list(await self.session.execute(query))  # TODO проверить что тут

    async def clear_purchases(self, tg_id: int) -> None:
        query = delete(PurchaseModel).where(PurchaseModel.user_id == tg_id)
        await self.session.execute(query)
        await self.session.flush()
