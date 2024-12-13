from tools.enums import StrEnum


class SlashCommand(StrEnum):
    START = "start"
    MENU = "menu"
    HELP = "help"
    PROFILE = "profile"
    ME = "me"
    BALANCE = "balance"


class TextCommand(StrEnum):
    START = "Старт"
    MENU = "Меню"
    HELP = "Помощь"
    PROFILE = "Профиль"
    BALANCE = "Баланс"


class BotWindow(StrEnum):
    MAIN_MENU = "main_menu"
    HELP = "help"
    PROFILE = "profile"
    ADMIN_PANEL = "admin_panel"
    NOTIFY = "notify"
    SHOP = "shop"
    CART = "cart"
    TRANSFER_FUNDS = "transfer_fund"
