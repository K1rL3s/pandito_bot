import contextlib

from aiogram.exceptions import TelegramAPIError
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.input import MessageInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.dialogs.flags import FORCE_GET_USER_KEY
from bot.handlers.client.menu.states import MenuStates
from core.services.users import UsersService
from database.models import UserModel
from database.repos.users import UsersRepo


@inject
async def id_input_handler(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
    users_repo: FromDishka[UsersRepo],
) -> None:
    receiver_id = int(message.text)

    if receiver_id == message.from_user.id:
        text = "Нельзя сделать перевод самому себе :("
        await message.answer(text=text)
        return

    receiver = await users_repo.get_by_id(receiver_id)
    if not receiver:
        text = f"Пользователя с ID {receiver_id} не существует :("
        await message.answer(text=text)
        return

    manager.dialog_data["receiver_id"] = receiver.id
    manager.dialog_data["receiver_name"] = receiver.name
    await manager.next()


@inject
async def amount_input_handler(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
    users_service: FromDishka[UsersService],
) -> None:
    amount = int(message.text.strip())
    user: UserModel = dialog_manager.middleware_data["user"]

    if user.balance < amount:
        text = "У вас недостаточно коинов для перевода, введите другую сумму"
        await message.answer(text=text)
        return

    receiver_id: int = dialog_manager.dialog_data["receiver_id"]
    await users_service.transfer_funds(user.id, receiver_id, int(amount))

    with contextlib.suppress(TelegramAPIError):  # TODO сделать норм
        await message.bot.send_message(
            chat_id=receiver_id,
            text=f"Вам перевели {amount} Ит.!",
        )

    text = "Операция прошла успешно!"
    await message.answer(text=text)

    await dialog_manager.start(
        state=MenuStates.menu,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
        data={FORCE_GET_USER_KEY: True},
    )
