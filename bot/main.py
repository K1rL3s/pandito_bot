import asyncio
import re
from os import getenv

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandObject, CommandStart, StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    BotCommand,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    Message
)
from database import DB

TOKEN = getenv("TOKEN")
DATABASE_URL = (f"postgres://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}@{getenv('POSTGRES_HOST')}:"
                f"{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}?sslmode=disable")
OWNER = int(getenv("OWNER"))

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
db = DB()


class Registration(StatesGroup):
    name = State()
    confirm = State()


class TransferFunds(StatesGroup):
    receiver_id = State()
    amount = State()


class ViewProductCallback(CallbackData, prefix="view"):
    id: int


class BuyProductCallback(CallbackData, prefix="buy"):
    id: int


class StartStage(StatesGroup):
    participant_id = State()
    reward_amount = State()


class SalesmanShop(StatesGroup):
    product_id = State()
    buyer_id = State()


class SalesmanCart(StatesGroup):
    buyer_id = State()


async def generate_main_menu(user):
    stage = user.get("stage", 0)
    if stage == 0:  # участник
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Магазин 🛍️", callback_data="view_products"),
                 InlineKeyboardButton(text="Корзина 🧺", callback_data="purchases")],
                [InlineKeyboardButton(text="Перевод 💸", callback_data="transfer_funds"),
                 InlineKeyboardButton(text="Помощь 🆘", callback_data="help")]
            ]
        )
    elif stage == 1:  # этапщик
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Начать этап", callback_data="start_stage"),
                 InlineKeyboardButton(text="Помощь", callback_data="help")]
            ]
        )
    elif stage == 2:  # продавец
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Магазин продавца", callback_data="view_products_salesman"),
                 InlineKeyboardButton(text="Корзина участника", callback_data="members_purchases")],
                [InlineKeyboardButton(text="Помощь", callback_data="help")]
            ]
        )
    elif stage == 3:  # RTUITLab
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Начать этап", callback_data="start_stage"),
                 InlineKeyboardButton(text="Помощь", callback_data="help")]
            ]
        )
    else:
        await db.change_user_stage(user["stage"], 0)
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Магазин 🛍️", callback_data="view_products"),
                 InlineKeyboardButton(text="Корзина 🧺", callback_data="purchases")],
                [InlineKeyboardButton(text="Перевод 💸", callback_data="transfer_funds"),
                 InlineKeyboardButton(text="Помощь 🆘", callback_data="help")]
            ]
        )


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    if user:
        return

    await message.answer_sticker(r"CAACAgIAAxkBAAEM7c9nAwuUZBCLVlLpmPHfk4bNQcpXOwACHwADWbv8Jeo5dBvZPTaZNgQ")
    await message.answer("Привет! 👋\n\n"
                         "Меня зовут <b>Пандито!</b> 🐼\n"
                         "Я буду хранить твои <u>Иткоины</u> и оповещать тебя о всех важных событиях, "
                         "приуроченных Дню рождения Института информационных технологий!\n\n"
                         "Чтобы зарегистрироваться введи свою <b>фамилию</b> и <b>имя</b>\n<i>"
                         "(Пример: Иванов Ваня)</i>",
                         parse_mode="HTML")
    await state.set_state(Registration.name)


@dp.message(StateFilter(Registration.name))
async def reg_name(message: Message, state: FSMContext):
    full_name = message.text.strip()
    if not re.match(r"^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+$", full_name):
        await message.answer("Неверный формат!")
        return

    await state.update_data(full_name=full_name)
    confirm_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Подтвердить", callback_data="yes"),
             InlineKeyboardButton(text="Отмена", callback_data="no")]
        ]
    )
    await message.answer(f"Проверьте введенные данные!\n\nВас зовут <b>{full_name}</b>?",
                         reply_markup=confirm_kb,
                         parse_mode="HTML")
    await state.set_state(Registration.confirm)
    await state.update_data(name=full_name)


@dp.callback_query(StateFilter(Registration.confirm), F.data == "yes")
async def reg_confirm_yes(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    user_id = await db.create_user(
        callback.from_user.id, state_data["name"], callback.from_user.id == OWNER
    )
    kb = [[KeyboardButton(text="/menu")]]
    kb_menu = ReplyKeyboardMarkup(keyboard=kb,
                                  resize_keyboard=True,
                                  one_time_keyboard=True)
    await callback.message.delete()

    await callback.message.answer_sticker(r"CAACAgIAAxkBAAEM7dhnAxdZxlqB__bt8a5GR5wo9-vxJAACDQADWbv8JS5RHx3i_HUDNgQ")
    await callback.message.answer(
        f"Вы успешно зарегистрировались! 🎉\n\n<b>Ваш id: {user_id}</b>\n\n"
        f"Теперь вы можете вызывать <b>меню</b> командой <i>/menu</i>",
        reply_markup=kb_menu,
        parse_mode="HTML"
    )
    await state.clear()


@dp.callback_query(StateFilter(Registration.confirm), F.data == "no")
async def reg_confirm_no(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_data({})
    await callback.message.answer("Бывает, попробуй еще раз!")
    await state.set_state(Registration.name)
    await callback.message.delete()


@dp.message(Command(commands=["menu"]))
async def menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer_sticker(r"CAACAgIAAxkBAAEM7eFnAzNGgGnjM59XOgjO_cpmrvdFhAACFwADWbv8Jfuhn7EBJTs2NgQ")
    user = await db.get_user(message.from_user.id)
    menu_kb = await generate_main_menu(user)

    await message.answer(
        f"<b>Главное меню</b>\n\nВаш id: {user['id']}\nБаланс: {user['balance']} <b>Ит</b>."
        f"{'\n\n<u>Вы — этапщик</u>\n' if user['stage'] == 1 else ''}"
        f"{'\n\n<u>Вы — продавец</u>\n' if user['stage'] == 2 else ''}"
        f"{'\n\n<u>Вы — RTUITLab</u>\n' if user['stage'] == 3 else ''}"
        f"{'\n\n<u>Вы — администратор</u>\n' if user['is_admin'] else ''}",
        reply_markup=menu_kb,
        parse_mode="HTML"
    )
    await message.delete()


@dp.callback_query(F.data == "cancel")
async def menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    user = await db.get_user(callback.from_user.id)
    menu_kb = await generate_main_menu(user)

    await callback.message.answer(
        f"<b>Главное меню</b>\n\nВаш id: {user['id']}\nБаланс: {user['balance']} <b>Ит</b>."
        f"{'\n\n<u>Вы — этапщик</u>\n' if user['stage'] == 1 else ''}"
        f"{'\n\n<u>Вы — продавец</u>\n' if user['stage'] == 2 else ''}"
        f"{'\n\n<u>Вы — RTUITLab</u>\n' if user['stage'] == 3 else ''}"
        f"{'\n\n<u>Вы — администратор</u>\n' if user['is_admin'] else ''}",
        reply_markup=menu_kb,
        parse_mode="HTML"
    )
    await callback.message.delete()


@dp.callback_query(F.data == "cancel")
async def cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.delete()


@dp.callback_query(F.data == "transfer_funds")
async def transfer_funds(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer()
    await state.set_state(TransferFunds.receiver_id)
    ckb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Отмена", callback_data="cancel")]]
    )
    await callback.message.answer("Введите id человека, которому хотите перевести <b>Иткоины</b>",
                                  reply_markup=ckb,
                                  parse_mode="HTML")


@dp.message(StateFilter(TransferFunds.receiver_id))
async def transfer_funds_id(message: Message, state: FSMContext):
    id = message.text.strip()
    if not re.match(r"^\d+$", id):
        await message.answer("Неверный формат!")
        return
    receiver = await db.get_user_by_id(int(id))
    if not receiver:
        ckb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Отмена", callback_data="cancel")]
            ]
        )
        await message.answer(f"Пользователя с id {id} не существует!", reply_markup=ckb)
        return
    ckb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Отмена", callback_data="cancel")]]
    )
    await state.update_data(receiver_id=id, receiver_tg=receiver["tg"])
    await state.set_state(TransferFunds.amount)
    await message.answer(
        f"Перевод будет произведен пользователю с именем <b>{receiver["name"]}</b>\n\n"
        f"Если всё верно введите сумму перевода",
        reply_markup=ckb,
        parse_mode="HTML"
    )


@dp.message(StateFilter(TransferFunds.amount))
async def transfer_funds_amount(message: Message, state: FSMContext):
    amount = message.text.strip()
    if not re.match(r"^\d+$", amount) or int(amount) == 0:
        await message.answer("Неверный формат!")
        return
    user = await db.get_user(message.from_user.id)
    ckb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отмена", callback_data="cancel")]
        ]
    )
    scb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Главное меню", callback_data="cancel")]
        ]
    )
    if user["balance"] < int(amount):
        await message.answer(
            "У вас недостаточно для перевода, введите другую сумму", reply_markup=ckb
        )
    data = await state.get_data()
    await db.transfer_funds(int(user["id"]), int(data["receiver_id"]), int(amount))
    await message.answer(
        "Операция прошла успешно!",
        reply_markup=scb
    )
    await bot.send_message(data["receiver_tg"], f"Вам перевели {amount.lstrip("0")} Ит.!")
    await state.clear()


@dp.callback_query(F.data == "view_products")
async def view_products(callback: CallbackQuery):
    await callback.answer()
    products = await db.get_available_products()
    user = await db.get_user(callback.from_user.id)
    c_bk = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="cancel")]
        ]
    )
    if products:
        product_kb = [
            [InlineKeyboardButton(
                text=f"{product["name"]} — {product["price"]} Ит.",
                callback_data=ViewProductCallback(id=int(product["id"])).pack(),
            )] for product in products
        ]
        product_kb.append([InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="cancel")])
        p_kb = InlineKeyboardMarkup(inline_keyboard=product_kb)

        await callback.message.answer(
            f"Список товаров 🛍️\n\nБаланс: {user["balance"]} Ит.", reply_markup=p_kb
        )
    else:
        await callback.message.answer("Упс, сейчас ничего в наличии нет", reply_markup=c_bk)
    await callback.message.delete()


@dp.callback_query(ViewProductCallback.filter())
async def view_product(callback: CallbackQuery, callback_data: ViewProductCallback):
    await callback.answer()
    await callback.message.delete()
    product = await db.get_product(callback_data.id)
    if int(product["stock"]) > 0:
        b_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"Купить - {product["price"]} Ит.",
                        callback_data=BuyProductCallback(id=int(product["id"])).pack(),
                    ),
                    InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="view_products"),
                ]
            ]
        )
        await callback.message.answer(
            f"{product["id"]}. <b>{product["name"]}</b>\n\n{product["description"]}",
            reply_markup=b_kb,
            parse_mode="HTML"
        )
    else:
        c_bk = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="view_products")]
            ]
        )
        await callback.message.answer("Упс, уже раскупили", reply_markup=c_bk)


@dp.callback_query(BuyProductCallback.filter())
async def buy_product(callback: CallbackQuery, callback_data: BuyProductCallback):
    await callback.answer()
    product = await db.get_product(callback_data.id)
    user = await db.get_user(callback.from_user.id)
    shop_bk = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Магазин", callback_data="view_products")]
        ]
    )
    if int(product["stock"]) > 0:
        if user["balance"] >= product["price"]:
            await db.buy_product(int(user["id"]), int(product["id"]), 1)
            await callback.message.answer("Товар оплачен и добавлен в корзину!", reply_markup=shop_bk)
        else:
            await callback.message.answer("Упс, у вас недостаточно <b>Иткоинов</b>!",
                                          reply_markup=shop_bk,
                                          parse_mode="HTML")
    else:
        await callback.message.answer("Упс, продукт уже раскупили", reply_markup=shop_bk)
    await callback.message.delete()


@dp.callback_query(F.data == "purchases")
async def purchases(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    user = await db.get_user(callback.from_user.id)
    purchases = await db.get_user_purchases(int(user["id"]))
    c_bk = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="cancel")]
        ]
    )
    if purchases:
        purchases_list = "\n".join(
            [f"{purchase['product_name']} x{purchase['quantity_purchased']}" for purchase in purchases]
        )

        full_message = (
            "<b>Купленные товары</b> 🧺\n\n"
            f"{purchases_list}\n\n"
            "Чтобы их забрать, подойдите к <u>магазину</u>, либо в <u>Отделение А-337</u>"
        )

        await callback.message.answer(
            full_message, reply_markup=c_bk, parse_mode="HTML"
        )
    else:
        await callback.message.answer("<b>Ваша корзина пуста</b>",
                                      reply_markup=c_bk,
                                      parse_mode="HTML")


@dp.callback_query(F.data == "help")
async def help_message(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    c_bk = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="cancel")]
        ]
    )

    await callback.message.answer(f"Если у вас возникли вопросы или сложности в функционале <b>Пандито</b> "
                                  f"— пишите @whatochka",
                                  reply_markup=c_bk,
                                  parse_mode="HTML")


# ------------------------------------------------------------------------------------------ Этапщик
@dp.callback_query(F.data == "start_stage")
async def start_stage(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StartStage.participant_id)
    await callback.message.delete()
    ckb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Отмена", callback_data="cancel")]]
    )
    await callback.message.answer("Введите id участника, который пришел на этап:", reply_markup=ckb)


@dp.message(StateFilter(StartStage.participant_id))
async def stage_participant_id(message: Message, state: FSMContext):
    participant_id = message.text.strip()
    if not re.match(r"^\d+$", participant_id):
        await message.answer("Неверный формат id! Попробуйте еще раз.")
        return

    # Проверяем, существует ли пользователь с таким id
    user_id = await db.get_user_by_id(int(participant_id))
    user = await db.get_user(message.from_user.id)
    if not user_id:
        await message.answer("Такого участника не существует.")
        return

    await state.update_data(participant_id=participant_id)

    if user["stage"] == 1:
        ckb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="10", callback_data="reward_10")],
                [InlineKeyboardButton(text="20", callback_data="reward_20")],
                [InlineKeyboardButton(text="30", callback_data="reward_30")]
            ]
        )
    else:
        ckb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="10", callback_data="reward_10")]
            ]
        )
    await state.set_state(StartStage.reward_amount)
    await message.answer("Выберите сумму для начисления:", reply_markup=ckb)


@dp.callback_query(StateFilter(StartStage.reward_amount), F.data.startswith("reward_"))
async def stage_reward(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    amount = int(callback.data.split("_")[1])  # Получаем число из callback_data (10, 20, 30)
    data = await state.get_data()
    user = await db.get_user(callback.from_user.id)
    participant_id = int(data['participant_id'])

    c_bk = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="start_stage")]
        ]
    )

    # Начисляем валюту
    await db.update_user_balance(participant_id, amount, user['id'])

    await callback.message.answer(f"Участнику с id {participant_id} начислено {amount} Ит.",
                                  reply_markup=c_bk)
    await state.clear()


# ------------------------------------------------------------------------------------------ Этапщик
# ------------------------------------------------------------------------------------------ Продавец
@dp.callback_query(F.data == "view_products_salesman")
async def view_products_salesman(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    products = await db.get_available_products()  # Получаем список товаров из базы данных
    if products:
        product_kb = [
            [InlineKeyboardButton(
                text=f"{product['name']} - {product['price']} Ит.",
                callback_data=f"salesman_select_product_{product['id']}"
            )] for product in products
        ]
        product_kb.append([InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="cancel")])
        p_kb = InlineKeyboardMarkup(inline_keyboard=product_kb)

        await callback.message.answer("Выберите товар для продажи:", reply_markup=p_kb)
    else:
        await callback.message.answer("В магазине нет товаров в наличии.")


@dp.callback_query(F.data.startswith("salesman_select_product_"))
async def salesman_select_product(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    product_id = int(callback.data.split("_")[-1])
    await state.update_data(product_id=product_id)
    await state.set_state(SalesmanShop.buyer_id)
    await callback.message.answer("Введите id покупателя, которому нужно продать товар.")


@dp.message(StateFilter(SalesmanShop.buyer_id))
async def salesman_buyer_id(message: Message, state: FSMContext):
    buyer_id = message.text.strip()
    if not re.match(r"^\d+$", buyer_id):
        await message.answer("Неверный формат id! Попробуйте еще раз.")
        return

    user = await db.get_user_by_id(int(buyer_id))
    if not user:
        await message.answer("Такого покупателя не существует.")
        return

    c_bk = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="view_products_salesman")]
        ]
    )

    data = await state.get_data()
    product_id = data['product_id']
    product = await db.get_product(product_id)

    if user['balance'] >= product['price']:
        # Если средств хватает, списываем деньги и уменьшаем количество товара
        await db.buy_product(int(buyer_id), int(product_id), 1)

        await message.answer(f"Успех! {user['name']} купил {product['name']} за "
                             f"{product['price']} Ит.",
                             reply_markup=c_bk)
    else:
        await message.answer("У покупателя недостаточно средств.", reply_markup=c_bk)

    await state.clear()


@dp.callback_query(F.data == "members_purchases")
async def view_members_purchases(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await state.set_state(SalesmanCart.buyer_id)
    await callback.message.answer("Введите id участника, чью корзину хотите просмотреть.")


@dp.message(StateFilter(SalesmanCart.buyer_id))
async def show_cart(message: Message, state: FSMContext):
    buyer_id = message.text.strip()
    if not re.match(r"^\d+$", buyer_id):
        await message.answer("Неверный формат id! Попробуйте еще раз.")
        return

    user = await db.get_user_by_id(int(buyer_id))
    if not user:
        await message.answer("Такого участника не существует.")
        return

    purchases = await db.get_user_purchases(int(buyer_id))

    c_bk = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="cancel")]
        ]
    )

    if purchases:
        cart_text = "\n".join(
            [f"{purchase['product_name']} x{purchase['quantity_purchased']}" for purchase in purchases])
        confirm_kb = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Подтвердить", callback_data=f"confirm_clear_cart_{buyer_id}")]]
        )
        await message.answer(f"Корзина участника {user['name']}:\n\n{cart_text}", reply_markup=confirm_kb)
    else:
        await message.answer("Корзина пуста.", reply_markup=c_bk)

    await state.clear()


@dp.callback_query(F.data.startswith("confirm_clear_cart_"))
async def confirm_clear_cart(callback: CallbackQuery):
    buyer_id = int(callback.data.split("_")[-1])

    # Очищаем корзину участника в базе данных
    await db.clear_user_purchases(buyer_id)

    c_bk = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад 🔙", callback_data="cancel")]
        ]
    )

    await callback.message.answer(f"Корзина участника с id {buyer_id} успешно очищена!", reply_markup=c_bk)
    await callback.message.delete()


@dp.message(Command(commands=["broadcast"]), StateFilter(None))
async def admin_broadcast(message: Message, command: CommandObject):
    user = await db.get_user(message.from_user.id)
    if not user["is_admin"]:
        await message.delete()
        return
    if command.args:
        text = command.args
        users = await db.get_all_users()
        for user in users:
            await bot.send_message(user["tg"], text)
        await message.answer("Успешный успех")
    else:
        await message.answer("Формат: /broadcast <message>")


@dp.message(Command(commands=["money"]), StateFilter(None))
async def admin_add_money(message: Message, command: CommandObject):
    user = await db.get_user(message.from_user.id)
    if not user["is_admin"]:
        await message.delete()
        return
    if command.args and len(command.args.split()) == 2:
        args = command.args.split()
        user_id, amount = int(args[0]), int(args[1])
        await db.update_user_balance(user_id, amount, user["id"])
        await message.answer(f"Добавлено {amount} пользователю {user_id}")
    else:
        await message.answer("Формат: /money <user_id> <amount>")


@dp.message(Command(commands=["stage"]), StateFilter(None))
async def admin_change_stage(message: Message, command: CommandObject):
    user = await db.get_user(message.from_user.id)
    if not user["is_admin"]:
        await message.delete()
        return
    if command.args and len(command.args.split()) == 2:
        args = command.args.split()
        user_id, stage = int(args[0]), int(args[1])
        await db.change_user_stage(user_id, stage)
        await message.answer("Успех!")
    else:
        await message.answer("Формат: /stage <user_id> <stage>")


@dp.message(Command(commands=["product"]), StateFilter(None))
async def admin_new_product(message: Message, command: CommandObject):
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


@dp.message(Command(commands=["stock"]), StateFilter(None))
async def admin_update_stock(message: Message, command: CommandObject):
    user = await db.get_user(message.from_user.id)
    if not user["is_admin"]:
        await message.delete()
        return

    if command.args and len(command.args.split()) == 2:
        args = command.args.split()
        product_id, new_stock = int(args[0]), int(args[1])

        # Обновляем количество товара
        updated_stock = await db.update_product_stock(product_id, new_stock)
        if updated_stock is not None:
            await message.answer(f"Количество товара с ID {product_id} обновлено до {new_stock}")
        else:
            await message.answer(f"Ошибка: Не удалось обновить товар с ID {product_id}")
    else:
        await message.answer("Формат: /stock <id> <new_stock>")


@dp.message(Command(commands=["price"]), StateFilter(None))
async def admin_change_product_price(message: Message, command: CommandObject):
    user = await db.get_user(message.from_user.id)
    if not user["is_admin"]:
        await message.delete()
        return

    if command.args and len(command.args.split()) == 2:
        args = command.args.split()
        product_id, new_price = int(args[0]), int(args[1])

        # Обновляем цену товара
        updated_price = await db.change_product_price(product_id, new_price)
        if updated_price is not None:
            await message.answer(f"Цена товара с ID {product_id} изменена на {new_price}")
        else:
            await message.answer(f"Ошибка: Не удалось обновить цену для товара с ID {product_id}")
    else:
        await message.answer("Формат: /price <id> <new_price>")


@dp.message(Command(commands=["logs"]), StateFilter(None))
async def admin_view_logs(message: Message, command: CommandObject):
    user = await db.get_user(message.from_user.id)
    if not user["is_admin"]:
        await message.delete()
        return
    if command.args and len(command.args.split()) == 1:
        user_id = int(command.args.strip())
        logs = await db.get_user_logs(user_id)
        log_texts = [f"{log['created_at']}: {log['description']}" for log in logs][:10]
        await message.answer("\n".join(log_texts) or "Нет логов")
    else:
        await message.answer("Формат: /logs <user_id>")


@dp.message(Command(commands=["list_users"]))
async def list_users(message: Message):
    user = await db.get_user(message.from_user.id)
    if not user["is_admin"]:
        await message.answer("У вас нет прав для выполнения этой команды.")
        return

    users = await db.get_all_users()
    if users:
        user_list = "\n".join(
            [f"ID: {user['id']}, ФИО: {user['name']}, Баланс: {user['balance']} Ит." for user in users])
        await message.answer(f"<b>Список участников:</b>\n\n{user_list}", parse_mode="HTML")
    else:
        await message.answer("Нет зарегистрированных участников.")


@dp.message(Command(commands=["delete_product"]), StateFilter(None))
async def admin_delete_product(message: Message, command: CommandObject):
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


@dp.message(Command(commands=["list_products"]), StateFilter(None))
async def admin_list_products(message: Message):
    user = await db.get_user(message.from_user.id)
    if not user["is_admin"]:
        await message.answer("У вас нет прав для выполнения этой команды.")
        return

    products = await db.get_all_products()
    if products:
        product_list = "\n".join([
                                     f"ID: {product['id']}, Название: {product['name']}, Цена: {product['price']} Ит., "
                                     f"Остаток: {product['stock']}"
                                     for product in products])
        await message.answer(f"<b>Список товаров:</b>\n\n{product_list}", parse_mode="HTML")
    else:
        await message.answer("Нет товаров.")


@dp.message(StateFilter(None))
async def unknown_msg(message: Message):
    await message.delete()


async def main():
    global db
    await db.init(DATABASE_URL)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands([BotCommand(command="menu", description="Меню")])
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
