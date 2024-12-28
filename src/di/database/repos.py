from dishka import Provider, Scope, provide

from database.repos.logs import LogsRepo
from database.repos.products import ProductsRepo
from database.repos.purchases import PurchasesRepo
from database.repos.secrets import SecretsRepo
from database.repos.users import UsersRepo


class ReposProvider(Provider):
    logs_repo = provide(LogsRepo, scope=Scope.REQUEST)
    products_repo = provide(ProductsRepo, scope=Scope.REQUEST)
    purchases_repo = provide(PurchasesRepo, scope=Scope.REQUEST)
    users_repo = provide(UsersRepo, scope=Scope.REQUEST)
    secrets_repo = provide(SecretsRepo, scope=Scope.REQUEST)
