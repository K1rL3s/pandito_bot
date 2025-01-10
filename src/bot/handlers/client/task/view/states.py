from aiogram.fsm.state import State, StatesGroup


class ViewTaskStates(StatesGroup):
    task = State()
    cancel = State()
