from aiogram.fsm.state import State, StatesGroup


class ViewSecretsStates(StatesGroup):
    list = State()
    one = State()
    confirm = State()
