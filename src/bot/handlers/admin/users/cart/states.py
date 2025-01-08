from aiogram.fsm.state import State, StatesGroup


class CartUserStates(StatesGroup):
    cart = State()
    clear = State()
    confirm = State()
