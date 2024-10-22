import asyncio
import sys

from bots.factories.bot import create_bot
from bots.factories.dispatcher import create_dispatcher, create_storage
from run.runners.polling import run_polling
from run.runners.webhook import run_token_based_webhook
from configs.app import create_app_config_from_env


def main() -> None:
    config = create_app_config_from_env()

    storage = create_storage()
    dp = create_dispatcher(debug_name="__child_bots__", storage=storage)

    bots = [create_bot(token=token) for token in []]  # TODO: Брать токены из БД

    if config.telegram.use_webhook:
        return run_token_based_webhook(dp=dp, config=config)
    return run_polling(dp=dp, bots=bots)


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()
