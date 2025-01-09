from aiogram.fsm.state import State, StatesGroup


class ViewTasksStates(StatesGroup):
    list = State()
    one = State()
    confirm = State()
