from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.ids import ProductId
from database.repos.products import ProductsRepo


@inject
async def get_all_products(
    dialog_manager: DialogManager,
    products_repo: FromDishka[ProductsRepo],
    **__: Any,
) -> dict[str, Any]:
    products = await products_repo.get_all()
    return {"products": products}


@inject
async def get_one_product(
    dialog_manager: DialogManager,
    products_repo: FromDishka[ProductsRepo],
    **__: Any,
) -> dict[str, Any]:
    product_id: ProductId = dialog_manager.dialog_data["product_id"]
    product = await products_repo.get_by_id(product_id)
    return {"product": product}
