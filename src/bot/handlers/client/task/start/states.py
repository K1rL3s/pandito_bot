from aiogram.fsm.state import State, StatesGroup


class StartTaskStates(StatesGroup):
    wait = State()
    started = State()
