from sqlalchemy import delete, select, update

from database.models.products import ProductModel
from database.repos.base import BaseAlchemyRepo


class ProductsRepo(BaseAlchemyRepo):
    async def create_product(
        self,
        name: str,
        description: str,
        price: int,
        stock: int,
    ) -> int:
        product = ProductModel(
            name=name,
            description=description,
            price=price,
            stock=stock,
        )
        self.session.add(product)
        await self.session.commit()
        return product.id  # TODO проверить что айди есть

    async def get_one(self, product_id: int) -> ProductModel | None:
        query = select(ProductModel).where(ProductModel.id == product_id)
        return await self.session.scalar(query)

    async def get_available(self) -> list[ProductModel]:
        query = select(ProductModel).where(ProductModel.stock > 0)
        return list(await self.session.scalars(query))

    async def get_all(self) -> list[ProductModel]:
        query = select(ProductModel)
        return list(await self.session.scalars(query))

    async def set_stock(self, product_id: int, new_stock: int) -> int:
        query = (
            update(ProductModel)
            .where(ProductModel.id == product_id)
            .values(stock=new_stock)
        )
        await self.session.execute(query)
        await self.session.commit()
        return new_stock

    async def set_price(self, product_id: int, new_price: int) -> int:
        query = (
            update(ProductModel)
            .where(ProductModel.id == product_id)
            .values(price=new_price)
        )
        await self.session.execute(query)
        await self.session.commit()
        return new_price

    async def delete(self, product_id: int) -> None:
        query = delete(ProductModel).where(ProductModel.id == product_id)
        await self.session.execute(query)
        await self.session.commit()
