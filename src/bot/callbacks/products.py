from aiogram.filters.callback_data import CallbackData


class ViewProductCallback(CallbackData, prefix="view"):
    id: int


class BuyProductCallback(CallbackData, prefix="buy"):
    id: int
