from dishka import Provider, Scope, provide

from core.services.broadcast import Broadcaster
from core.services.products import ProductsService
from core.services.qrcodes import QRCodeService
from core.services.secrets import SecretsService
from core.services.tasks import TasksService
from core.services.users import UsersService


class ServicesProvider(Provider):
    scope = Scope.REQUEST

    qrcode_service = provide(QRCodeService, scope=Scope.APP)
    products_service = provide(ProductsService)
    users_service = provide(UsersService)
    broadcaster = provide(Broadcaster)
    secrets_service = provide(SecretsService)
    tasks_service = provide(TasksService)
