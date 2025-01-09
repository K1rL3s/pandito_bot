from core.enums import ALL_ROLES, RightsRole
from core.exceptions import NotRightRole, RoleNotFound, UserNotFound
from core.ids import UserId
from database.repos.users import UsersRepo


class RolesService:
    def __init__(self, users_repo: UsersRepo) -> None:
        self.users_repo = users_repo

    async def is_admin(self, user_id: UserId) -> bool:
        return await self.is_enough_rights(user_id, RightsRole.ADMIN)

    async def is_seller(self, user_id: UserId) -> bool:
        return await self.is_enough_rights(user_id, RightsRole.SELLER)

    async def is_stager(self, user_id: UserId) -> bool:
        return await self.is_enough_rights(user_id, RightsRole.STAGER)

    async def is_lottery(self, user_id: UserId) -> bool:
        return await self.is_enough_rights(user_id, RightsRole.LOTTERY)

    async def is_enough_rights(self, user_id: UserId, role: RightsRole | None) -> bool:
        user = await self.users_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)

        if role not in ALL_ROLES:
            raise RoleNotFound(role)

        if user.role == role or user.role == RightsRole.ADMIN:
            return True

        raise NotRightRole(user_id, role)
