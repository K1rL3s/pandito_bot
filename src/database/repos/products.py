from sqlalchemy import select, update

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

    async def get_product(self, product_id: int) -> ProductModel | None:
        query = select(ProductModel).where(ProductModel.id == product_id)
        return await self.session.scalar(query)

    async def update_stock(self, product_id: int, new_stock: int) -> int:
        query = (
            update(ProductModel)
            .where(ProductModel.id == product_id)
            .values(stock=new_stock)
        )
        await self.session.execute(query)
        await self.session.commit()
        return new_stock

    async def update_price(self, product_id: int, new_price: int) -> int:
        query = (
            update(ProductModel)
            .where(ProductModel.id == product_id)
            .values(price=new_price)
        )
        await self.session.execute(query)
        await self.session.commit()
        return new_price

    async def get_available(self) -> list[ProductModel]:
        query = select(ProductModel).where(ProductModel.stock > 0)
        return list(await self.session.scalars(query))

    async def get_all(self) -> list[ProductModel]:
        query = select(ProductModel)
        return list(await self.session.scalars(query))

    # TODO: в сервис
    async def buy_product(self, user_id: int, product_id: int, quantity: int):
        async with self.db_pool.acquire() as conn:
            sql = "SELECT buy_product($1, $2, $3);"
            return await conn.fetchval(sql, user_id, product_id, quantity)

    # TODO: в сервис
    async def delete_product(self, product_id: int):
        async with self.db_pool.acquire() as conn:
            sql = "DELETE FROM products WHERE id = $1;"
            await conn.execute(sql, product_id)
