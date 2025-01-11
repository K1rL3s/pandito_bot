from aiogram.fsm.state import State, StatesGroup


class LotteryUserStates(StatesGroup):
    student_id = State()
    group = State()
