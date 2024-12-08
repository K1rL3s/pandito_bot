from aiogram import Router
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.types import Message

from database.repos.database import Database

router = Router(name=__file__)


@router.message(Command("product"), StateFilter(None))
async def admin_new_product(message: Message, command: CommandObject, db: Database):
    user = await db.get_user(message.from_user.id)
    if not user["is_admin"]:
        await message.delete()
        return
    if command.args and len(command.args.split()) >= 4:
        args = command.args.split()
        name, price, stock, description = args[0], int(args[1]), int(args[2]), args[3:]
        id = await db.create_product(name, " ".join(description), price, stock)
        await message.answer(f"Успех! Id: {id}")
    else:
        await message.answer("Формат: /product <name> <price> <stock> <description>")


@router.message(Command(commands=["stock"]), StateFilter(None))
async def admin_update_stock(message: Message, command: CommandObject, db: Database):
    user = await db.get_user(message.from_user.id)
    if not user["is_admin"]:
        await message.delete()
        return

    if command.args and len(command.args.split()) == 2:
        args = command.args.split()
        product_id, new_stock = int(args[0]), int(args[1])

        # Обновляем количество товара
        updated_stock = await db.set_stock(product_id, new_stock)
        if updated_stock is not None:
            await message.answer(
                f"Количество товара с ID {product_id} обновлено до {new_stock}",
            )
        else:
            await message.answer(f"Ошибка: Не удалось обновить товар с ID {product_id}")
    else:
        await message.answer("Формат: /stock <id> <new_stock>")


@router.message(Command(commands=["price"]), StateFilter(None))
async def admin_change_product_price(
    message: Message,
    command: CommandObject,
    db: Database,
):
    user = await db.get_user(message.from_user.id)
    if not user["is_admin"]:
        await message.delete()
        return

    if command.args and len(command.args.split()) == 2:
        args = command.args.split()
        product_id, new_price = int(args[0]), int(args[1])

        # Обновляем цену товара
        updated_price = await db.set_price(product_id, new_price)
        if updated_price is not None:
            await message.answer(
                f"Цена товара с ID {product_id} изменена на {new_price}",
            )
        else:
            await message.answer(
                f"Ошибка: Не удалось обновить цену для товара с ID {product_id}",
            )
    else:
        await message.answer("Формат: /price <id> <new_price>")


@router.message(Command(commands=["delete_product"]), StateFilter(None))
async def admin_delete_product(message: Message, command: CommandObject, db: Database):
    user = await db.get_user(message.from_user.id)
    if not user["is_admin"]:
        await message.delete()
        return
    if command.args and len(command.args.split()) == 1:
        product_id = int(command.args)
        await db.delete_product(product_id)
        await message.answer(f"Товар с ID {product_id} был успешно удален.")
    else:
        await message.answer("Формат: /delete_product <id>")


@router.message(Command(commands=["list_products"]), StateFilter(None))
async def admin_list_products(message: Message, db: Database):
    user = await db.get_user(message.from_user.id)
    if not user["is_admin"]:
        await message.answer("У вас нет прав для выполнения этой команды.")
        return

    products = await db.get_all()
    if products:
        product_list = "\n".join(
            [
                f"ID: {product['id']}, Название: {product['name']}, Цена: {product['price']} Ит., "
                f"Остаток: {product['stock']}"
                for product in products
            ],
        )
        await message.answer(
            f"<b>Список товаров:</b>\n\n{product_list}",
            parse_mode="HTML",
        )
    else:
        await message.answer("Нет товаров.")
