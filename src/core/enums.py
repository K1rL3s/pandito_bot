from tools.enums import StrEnum, ValuesEnum


class RightsRole(StrEnum, ValuesEnum):
    ADMIN = "admin"
    SELLER = "seller"
    STAGER = "stager"
    LOTTERY = "lottery"


ALL_ROLES = (*enumerate(RightsRole.values()), (len(RightsRole.values()), None))
