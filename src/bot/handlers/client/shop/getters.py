from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.ids import ProductId
from database.models import ProductModel
from database.repos.products import ProductsRepo


@inject
async def get_available_products(
    products_repo: FromDishka[ProductsRepo],
    **__: Any,
) -> dict[str, list[ProductModel]]:
    products = await products_repo.get_available()
    total_stock = sum(product.stock for product in products)
    return {
        "products": products,
        "products_len": len(products),
        "total_stock": total_stock,
    }


@inject
async def get_one_product(
    dialog_manager: DialogManager,
    products_repo: FromDishka[ProductsRepo],
    **__: Any,
) -> dict[str, ProductModel | None]:
    product_id: ProductId = dialog_manager.dialog_data["product_id"]
    return {"product": await products_repo.get_one(product_id)}
