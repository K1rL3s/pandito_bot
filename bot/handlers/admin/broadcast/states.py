from aiogram.fsm.state import State, StatesGroup


class BroadcastStates(StatesGroup):
    wait = State()
    confirm = State()
