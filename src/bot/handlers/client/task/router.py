from aiogram import F, Router
from aiogram.filters import CommandStart, MagicData
from aiogram.types import Message

router = Router(name=__file__)


@router.message(
    CommandStart(deep_link=True, magic=F.args.startswith("task_")),
    MagicData(F.command.args.as_("task_deeplink")),
)
async def start_task_by_deeplink(
    message: Message,
    task_deeplink: str,
) -> None:
    _prefix, task_id = task_deeplink.split("_", maxsplit=1)
    await message.answer(text=task_id)
