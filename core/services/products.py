from core.exceptions import (
    InvalidValue,
    NotEnoughMoney,
    NotEnoughStock,
    ProductNotFound,
    UserNotFound,
)
from database.repos.logs import LogsRepo
from database.repos.products import ProductsRepo
from database.repos.purchases import PurchasesRepo
from database.repos.users import UsersRepo


class ProductsService:
    def __init__(
        self,
        products_repo: ProductsRepo,
        users_repo: UsersRepo,
        purchases_repo: PurchasesRepo,
        logs_repo: LogsRepo,
    ) -> None:
        self.products_repo = products_repo
        self.users_repo = users_repo
        self.purchases_repo = purchases_repo
        self.logs_repo = logs_repo

    async def buy_product(self, user_id: int, product_id: int, quantity: int) -> int:
        product = await self.products_repo.get_one(product_id)
        if product is None:
            raise ProductNotFound(product_id)

        if product.stock < quantity:
            raise NotEnoughStock(product.stock, quantity)

        user = await self.users_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)

        total_price = product.price * quantity
        if user.balance < total_price:
            raise NotEnoughMoney(user.balance, total_price)

        new_balance = user.balance - total_price
        await self.users_repo.set_balance(user.id, new_balance)

        new_stock = product.stock - quantity
        await self.products_repo.set_stock(product_id, new_stock)

        await self.purchases_repo.create(user.id, product_id, quantity)

        await self.logs_repo.log_action(
            user.id,
            f"Bought {quantity} of {product_id} for {quantity} units",
        )

        return new_balance

    async def decrement_stock(self, product_id: int, quantity: int) -> int:
        if quantity <= 0:
            raise InvalidValue(
                "Нельзя уменьшить кол-во товара на отрицательное значение "
                f'"{quantity}"',
            )

        product = await self.products_repo.get_one(product_id)
        if product is None:
            raise ProductNotFound(product_id)

        if product.stock < quantity:
            raise NotEnoughStock(product.stock, quantity)

        new_stock = product.stock - quantity
        await self.products_repo.set_stock(product_id, new_stock)

        return new_stock

    async def set_stock(self, product_id: int, new_stock: int) -> int:
        if new_stock < 0:
            raise InvalidValue("Кол-во товара не может быть отрицательным")

        product = await self.products_repo.get_one(product_id)
        if product is None:
            raise ProductNotFound(product_id)

        return await self.products_repo.set_stock(product_id, new_stock)

    async def set_price(self, product_id: int, new_price: int) -> int:
        if new_price <= 0:
            raise InvalidValue("Цена не может быть отрицательной")

        product = await self.products_repo.get_one(product_id)
        if product is None:
            raise ProductNotFound(product_id)

        return await self.products_repo.set_price(product_id, new_price)
