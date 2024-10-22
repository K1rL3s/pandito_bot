from typing import Any

from aiogram import Bot, Dispatcher, loggers

from configs.app import AppConfig


async def polling_startup(bots: list[Bot], config: AppConfig) -> None:
    for bot in bots:
        await bot.delete_webhook(
            drop_pending_updates=config.telegram.drop_pending_updates,
        )
    if config.telegram.drop_pending_updates:
        loggers.dispatcher.info("Updates skipped successfully")


def run_polling(dp: Dispatcher, bots: list[Bot], **kwargs: Any) -> None:
    dp.startup.register(polling_startup)
    return dp.run_polling(*bots, **kwargs)
