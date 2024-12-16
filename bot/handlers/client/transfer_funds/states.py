from aiogram.fsm.state import State, StatesGroup


class TransferFundsStates(StatesGroup):
    id = State()
    amount = State()
    confirm = State()
