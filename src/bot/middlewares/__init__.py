from aiogram import Bot, Dispatcher

from bot.middlewares.outer.callback_answer import CallbackAnswerMiddleware
from bot.middlewares.outer.throttling import ThrottlingMiddleware
from bot.middlewares.outer.user_context import UserDbContextMiddleware
from bot.middlewares.request.retry import RetryRequestMiddleware

__all__ = ("setup_middlewares",)


def setup_middlewares(bot: Bot, dp: Dispatcher) -> None:
    bot.session.middleware(RetryRequestMiddleware())

    dp.callback_query.outer_middleware(CallbackAnswerMiddleware())

    dp.update.outer_middleware(ThrottlingMiddleware())

    dp.update.outer_middleware(UserDbContextMiddleware())
