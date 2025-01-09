from core.enums import RightsRole
from core.ids import ProductId, UserId


class ServiceException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self}')"


class EntityAlreadyExists(ServiceException):
    pass


class SecretAlreadyExists(EntityAlreadyExists):
    def __init__(self, phrase: str) -> None:
        self.message = f'Секрет с фразой "{phrase}" уже существует'


class EntityNotFound(ServiceException):
    pass


class UserNotFound(EntityNotFound):
    def __init__(self, user_id: UserId) -> None:
        self.message = f"Пользователь с айди {user_id} не найден"


class ProductNotFound(EntityNotFound):
    def __init__(self, product_id: ProductId) -> None:
        self.message = f"Товар с айди {product_id} не найден"


class RoleNotFound(EntityNotFound):
    def __init__(self, role: str) -> None:
        self.message = f'Роль "{role}" не найдена'


class NotEnoughStock(ServiceException):
    def __init__(self, current_stock: int, excepted_stock: int) -> None:
        self.message = (
            "Недостаточное кол-во товара.\n"
            f"Текущее: {current_stock}, ожидаемое: {excepted_stock}"
        )


class NotEnoughMoney(ServiceException):
    def __init__(self, current_balance: int, excepted_balance: int) -> None:
        self.message = (
            "Недостаточно Пятаков на балансе.\n"
            f"Текущее: {current_balance}, ожидаемое: {excepted_balance}"
        )


class InvalidValue(ServiceException):
    pass


class InvalidValueAfterUpdate(ServiceException):
    pass


class NotEnoughRights(ServiceException):
    pass


class NotRightRole(NotEnoughRights):
    def __init__(self, user_id: UserId, role: RightsRole | None) -> None:
        self.message = f"Пользователь с айди {user_id} не является {role}"


class NotAdmin(NotRightRole):
    def __init__(self, user_id: UserId) -> None:
        super().__init__(user_id, RightsRole.ADMIN)
