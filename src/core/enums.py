from tools.enums import StrEnum, ValuesEnum


class RightsRole(StrEnum, ValuesEnum):
    ADMIN = "admin"
    SELLER = "seller"
    STAGER = "stager"
    LOTTERY = "lottery"
