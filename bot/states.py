from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    name = State()
    confirm = State()


class TransferFunds(StatesGroup):
    receiver_id = State()
    amount = State()


class StartStage(StatesGroup):
    participant_id = State()
    reward_amount = State()


class SalesmanShop(StatesGroup):
    product_id = State()
    buyer_id = State()


class SalesmanCart(StatesGroup):
    buyer_id = State()
