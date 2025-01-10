from aiogram.fsm.state import State, StatesGroup


class TaskUserStates(StatesGroup):
    task = State()
