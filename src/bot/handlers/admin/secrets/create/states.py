from aiogram.fsm.state import State, StatesGroup


class CreateSecretStates(StatesGroup):
    phrase = State()
    reward = State()
    activation_limit = State()
    confirm = State()
