from typing import Any

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common.when import Whenable

from core.enums import RightsRole
from database.models import UserModel


class RoleAccess:
    def __init__(self, roles: list[RightsRole]) -> None:
        self.roles = roles

    def __call__(
        self,
        data: dict[str, Any],
        widget: Whenable,
        dialog_manager: DialogManager,
    ) -> bool:
        user: UserModel = data["middleware_data"]["user"]
        return user.role in self.roles


class IsAdmin(RoleAccess):
    def __init__(self) -> None:
        super().__init__([RightsRole.ADMIN])


class IsSeller(RoleAccess):
    def __init__(self) -> None:
        super().__init__([RightsRole.SELLER, RightsRole.ADMIN])


class IsStager(RoleAccess):
    def __init__(self) -> None:
        super().__init__([RightsRole.STAGER, RightsRole.ADMIN])


class IsLottery(RoleAccess):
    def __init__(self) -> None:
        super().__init__([RightsRole.LOTTERY, RightsRole.ADMIN])


class IsWithRole(RoleAccess):
    def __init__(self) -> None:
        super().__init__(RightsRole.values())
