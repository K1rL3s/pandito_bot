from aiogram.filters.callback_data import CallbackData


class OpenWindow(CallbackData, prefix="open_window"):
    window: str
