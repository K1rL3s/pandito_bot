from typing import Any

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


def create_bot(
    token: str,
    parse_mode: str = ParseMode.HTML,
    **kwargs: Any,
) -> Bot:
    return Bot(
        token=token,
        default=DefaultBotProperties(
            parse_mode=parse_mode,
            **{"link_preview_is_disabled": True, **kwargs},
        ),
    )


async def set_commands(bot: Bot, commands: dict[str, str]) -> None:
    await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in commands.items()
        ],
        scope=BotCommandScopeAllPrivateChats(),
    )
