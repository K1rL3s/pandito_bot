from aiogram import Bot, Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import Chat, ErrorEvent

from core.exceptions import ServiceException

router = Router(name=__file__)


@router.error(ExceptionTypeFilter(ServiceException))
async def service_exceptions_handler(
    event: ErrorEvent,
    bot: Bot,
    event_chat: Chat,
) -> None:
    text = (
        "😵‍💫 Произошла ошибка, попробуйте ещё раз. Вот её текст:\n\n"
        f"{event.exception!s}"
    )
    await bot.send_message(chat_id=event_chat.id, text=text)

    raise event.exception


@router.error(ExceptionTypeFilter(Exception))
async def all_exceptions_handler(
    event: ErrorEvent,
    bot: Bot,
    event_chat: Chat,
) -> None:
    text = (
        "❌😵 Произошла ошибка...\n"
        "Попробуйте ещё раз или напишите нам: @K1rLes @whatochka"
    )
    await bot.send_message(chat_id=event_chat.id, text=text)

    raise event.exception
