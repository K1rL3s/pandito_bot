from aiogram.fsm.state import State, StatesGroup


class ProductsStates(StatesGroup):
    list = State()
    one = State()
    final = State()
