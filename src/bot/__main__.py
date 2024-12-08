import asyncio
import logging
import sys

from dishka.integrations.aiogram import setup_dishka

from bot.config import get_bot_config
from bot.factory import create_bot, create_dispatcher
from bot.handlers import include_routers
from di.container import make_container


async def main() -> None:
    bot_config = get_bot_config()

    bot = create_bot(bot_config)
    dp = create_dispatcher()
    include_routers(dp)

    container = make_container()
    setup_dishka(container=container, router=dp, auto_inject=True)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        bot_config=bot_config,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
