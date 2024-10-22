import asyncio
import sys

from bots.factories.bot import create_bot
from bots.factories.dispatcher import create_dispatcher, create_storage
from infrastructure.redis.factory import create_redis
from run.runners.polling import run_polling
from run.runners.webhook import run_token_based_webhook
from configs.app import create_app_config_from_env


def main() -> None:
    config = create_app_config_from_env()
    redis = create_redis(config.redis) if config.redis else None

    storage = create_storage(redis=redis)
    dp = create_dispatcher(debug_name="__bot_father__", storage=storage)
    bot = create_bot(token=config.telegram.bot_father_token)

    if config.telegram.use_webhook:
        return run_token_based_webhook(dp=dp, config=config)
    return run_polling(dp=dp, bots=[bot], config=config)


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()
