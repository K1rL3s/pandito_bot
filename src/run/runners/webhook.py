from aiogram import Bot, Dispatcher, loggers
from aiogram.webhook.aiohttp_server import (
    BaseRequestHandler,
    setup_application,
    SimpleRequestHandler,
    TokenBasedRequestHandler,
)
from aiohttp import web

from configs.app import AppConfig


async def webhook_startup(dp: Dispatcher, bot: Bot, config: AppConfig) -> None:
    url = config.server.build_url(path=config.telegram.webhook_path)
    if await bot.set_webhook(
        url=url,
        allowed_updates=dp.resolve_used_update_types(),
        secret_token=config.telegram.webhook_secret,
        drop_pending_updates=config.telegram.drop_pending_updates,
    ):
        return loggers.webhook.info(
            "Main bot webhook successfully set on url '%s'", url
        )
    return loggers.webhook.error("Failed to set main bot webhook on url '%s'", url)


async def webhook_shutdown(bot: Bot, config: AppConfig) -> None:
    if not config.telegram.reset_webhook:
        return
    if await bot.delete_webhook():
        loggers.webhook.info("Dropped main bot webhook.")
    else:
        loggers.webhook.error("Failed to drop main bot webhook.")
    await bot.session.close()


def run_token_based_webhook(dp: Dispatcher, config: AppConfig) -> None:
    request_handler = TokenBasedRequestHandler(dispatcher=dp)
    _run_webhook(request_handler, dp, config)


def run_simple_webhook(dp: Dispatcher, bot: Bot, config: AppConfig) -> None:
    request_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=config.telegram.webhook_secret,
    )
    _run_webhook(request_handler, dp, config)


def _run_webhook(
    request_handler: BaseRequestHandler,
    dp: Dispatcher,
    config: AppConfig,
) -> None:
    app = web.Application()

    request_handler.register(app, path=config.telegram.webhook_path)

    setup_application(app, dp, config=config)
    app.update(**dp.workflow_data)

    dp.startup.register(webhook_startup)
    dp.shutdown.register(webhook_shutdown)

    return web.run_app(
        app=app,
        host=config.server.host,
        port=config.server.port,
    )
