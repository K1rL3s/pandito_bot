from aiogram.fsm.state import State, StatesGroup


class StartStates(StatesGroup):
    name = State()
    confirm = State()
    help = State()
