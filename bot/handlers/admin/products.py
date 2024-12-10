from aiogram import Router
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.types import Message
from dishka import FromDishka

from database.repos.products import ProductsRepo
from database.services.products import ProductsService

router = Router(name=__file__)


@router.message(Command("product"), StateFilter(None))
async def admin_new_product(
    message: Message,
    command: CommandObject,
    products_repo: FromDishka[ProductsRepo],
) -> None:
    if command.args and len(command.args.split()) >= 4:
        args = command.args.split()
        name, price, stock, description = args[0], int(args[1]), int(args[2]), args[3:]
        product = await products_repo.create_product(
            name,
            " ".join(description),
            price,
            stock,
        )
        await message.answer(f"Успех! Id: {product.id}")
    else:
        await message.answer(
            "Формат: /product <name> <price> <stock> <description>",
            parse_mode=None,
        )


@router.message(Command("stock"), StateFilter(None))
async def admin_update_stock(
    message: Message,
    command: CommandObject,
    products_service: FromDishka[ProductsService],
) -> None:
    if command.args and len(command.args.split()) == 2:
        args = command.args.split()
        product_id, new_stock = int(args[0]), int(args[1])
        await products_service.set_stock(product_id, new_stock)
        await message.answer(
            f"Количество товара с ID {product_id} обновлено до {new_stock}",
        )
    else:
        await message.answer("Формат: /stock <id> <new_stock>", parse_mode=None)


@router.message(Command("price"), StateFilter(None))
async def admin_change_product_price(
    message: Message,
    command: CommandObject,
    products_service: FromDishka[ProductsService],
) -> None:
    if command.args and len(command.args.split()) == 2:
        args = command.args.split()
        product_id, new_price = int(args[0]), int(args[1])
        await products_service.set_price(product_id, new_price)
        await message.answer(
            f"Цена товара с ID {product_id} изменена на {new_price}",
        )
    else:
        await message.answer("Формат: /price <id> <new_price>", parse_mode=None)


@router.message(Command("delete_product"), StateFilter(None))
async def admin_delete_product(
    message: Message,
    command: CommandObject,
    products_repo: FromDishka[ProductsRepo],
) -> None:
    if command.args and len(command.args.split()) == 1:
        product_id = int(command.args)
        await products_repo.delete(product_id)
        await message.answer(f"Товар с ID {product_id} был успешно удален.")
    else:
        await message.answer("Формат: /delete_product <id>", parse_mode=None)


@router.message(Command("list_products"), StateFilter(None))
async def admin_list_products(
    message: Message,
    products_repo: FromDishka[ProductsRepo],
) -> None:
    products = await products_repo.get_all()
    product_list = "\n".join(
        [
            f"ID: {product.id}, Название: {product.name}, "
            f"Цена: {product.price} Ит., Остаток: {product.stock}"
            for product in products
        ],
    )
    await message.answer(
        f"<b>Список товаров:</b>\n\n{product_list}" if product_list else "Не товаров.",
    )
