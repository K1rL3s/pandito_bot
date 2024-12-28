from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from bot.enums import SlashCommand
from bot.handlers.client.transfer_funds.states import TransferFundsStates

router = Router(name=__file__)


@router.message(Command(SlashCommand.TRANSFER))
async def transfer_funds_handler(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        state=TransferFundsStates.id,
    )
