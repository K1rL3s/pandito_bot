import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from bots.child.handlers import include_routers
from infrastructure.database.repos import Database
from infrastructure.database.repos import DATABASE_URL


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    TOKEN = getenv("TOKEN")
    OWNER = int(getenv("OWNER"))

    bot = Bot(TOKEN)
    dp = Dispatcher()
    include_routers(dp)

    db = await Database.init(DATABASE_URL)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands([BotCommand(command="menu", description="Меню")])
    await dp.start_polling(bot, db=db, owner_id=OWNER)


if __name__ == "__main__":
    asyncio.run(main())
