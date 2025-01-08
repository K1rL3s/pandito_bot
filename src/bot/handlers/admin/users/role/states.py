from aiogram.fsm.state import State, StatesGroup


class RoleUserStates(StatesGroup):
    select = State()
    role = State()
    confirm = State()
