from aiogram.fsm.state import State, StatesGroup


class ViewSecretsStates(StatesGroup):
    list = State()
    one = State()
    confirm = State()


class CreateSecretStates(StatesGroup):
    phrase = State()
    reward = State()
    activation_limit = State()
    confirm = State()
