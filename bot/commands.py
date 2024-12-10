from enum import Enum


class SlashCommands(str, Enum):
    START = "start"
    MENU = "menu"


class TextCommands(str, Enum):
    START = "Старт"
    MENU = "Меню"
