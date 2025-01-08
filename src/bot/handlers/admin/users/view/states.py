from aiogram.fsm.state import State, StatesGroup


class ViewUserStates(StatesGroup):
    id = State()
    one = State()
