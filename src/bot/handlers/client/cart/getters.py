from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from database.models import ProductModel, PurchaseModel, UserModel
from database.repos.purchases import PurchasesRepo


@inject
async def get_purchases(
    dialog_manager: DialogManager,
    purchases_repo: FromDishka[PurchasesRepo],
    **__: Any,
) -> dict[str, Any]:
    user: UserModel = dialog_manager.middleware_data["user"]

    result = await purchases_repo.get_user_purchases(user.id)
    total_products = len({i[0].id for i in result})
    total_purchases = sum(i[1].quantity for i in result)
    purchases_list = format_purchases(result)

    return {
        "total_products": total_products,
        "total_purchases": total_purchases,
        "purchases_list": purchases_list,
    }


def format_purchases(purchases: list[tuple[ProductModel, PurchaseModel]]) -> str:
    product_to_purchases: dict[tuple[int, str], int] = {}
    for product, purchase in purchases:
        if (product.id, product.name) not in product_to_purchases:
            product_to_purchases[(product.id, product.name)] = 0
        product_to_purchases[(product.id, product.name)] += purchase.quantity

    return "\n".join(
        [
            f"<b>{key[1]}</b> — <i>x{value}</i>"
            for key, value in sorted(product_to_purchases.items(), key=lambda x: x[0])
        ],
    )
