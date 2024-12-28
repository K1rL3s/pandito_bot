from dishka import Provider, Scope, provide

from core.services.broadcast import Broadcaster
from core.services.products import ProductsService
from core.services.qrcodes import QRCodeService
from core.services.secrets import SecretsService
from core.services.users import UsersService


class ServicesProvider(Provider):
    products_service = provide(ProductsService, scope=Scope.REQUEST)
    users_service = provide(UsersService, scope=Scope.REQUEST)
    broadcaster = provide(Broadcaster, scope=Scope.REQUEST)
    secrets_service = provide(SecretsService, scope=Scope.REQUEST)
    qrcode_service = provide(QRCodeService, scope=Scope.APP)
