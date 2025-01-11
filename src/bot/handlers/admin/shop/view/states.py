from aiogram.fsm.state import State, StatesGroup


class ViewProductsStates(StatesGroup):
    list = State()
    one = State()
    confirm = State()
