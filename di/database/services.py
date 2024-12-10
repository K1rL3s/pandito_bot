from dishka import Provider, Scope, provide

from database.services.products import ProductsService
from database.services.users import UsersService


class ServicesProvider(Provider):
    products_service = provide(ProductsService, scope=Scope.REQUEST)
    users_service = provide(UsersService, scope=Scope.REQUEST)