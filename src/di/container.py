from dishka import AsyncContainer, Provider, make_async_container
from dishka.integrations.aiogram import AiogramProvider

from di.services import ServicesProvider

from .aiogram import AiogramBotProvider
from .database.repos import ReposProvider
from .database.session import DBProvider


def make_container(*extra_providers: Provider) -> AsyncContainer:
    return make_async_container(
        DBProvider(),
        ReposProvider(),
        ServicesProvider(),
        AiogramProvider(),
        AiogramBotProvider(),
        *extra_providers,
    )
