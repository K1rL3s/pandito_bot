from aiogram.fsm.state import State, StatesGroup


class AnswerTaskStates(StatesGroup):
    wait = State()
    ok = State()
    fail = State()
