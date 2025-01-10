from aiogram.fsm.state import State, StatesGroup


class ConfirmTaskStates(StatesGroup):
    confirm = State()
