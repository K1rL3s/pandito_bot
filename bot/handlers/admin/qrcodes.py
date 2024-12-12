from aiogram import F, Router
from aiogram.filters import CommandStart, MagicData
from aiogram.types import Message

router = Router(name=__file__)


@router.message(
    CommandStart(deep_link=True, magic=F.args.isdigit()),
    MagicData(F.command.args.cast(int).as_("user_id")),
)
async def open_user_by_deeplink(message: Message, user_id: int) -> None:
    await message.answer(f"uid=<code>{user_id}</code>")
