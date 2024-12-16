from aiogram.fsm.state import State, StatesGroup


class ShopStates(StatesGroup):
    list = State()
    one = State()
    final = State()
