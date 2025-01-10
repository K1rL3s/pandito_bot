from aiogram.fsm.state import State, StatesGroup


class CancelTaskStates(StatesGroup):
    cancel = State()
