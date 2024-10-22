import os
from dataclasses import dataclass


YES_CHARS = "1yYtT"


@dataclass
class TelegramConfig:
    bot_father_token: str
    drop_pending_updates: bool
    use_webhook: bool
    reset_webhook: bool
    webhook_path: str
    webhook_secret: str


def create_telegram_config_from_env() -> TelegramConfig:
    bot_father_token = os.getenv("BOT_FATHER_TOKEN")
    drop_pending_updates = os.getenv("TELEGRAM_DROP_UPDATES") in YES_CHARS
    use_webhook = os.getenv("TELEGRAM_USE_WEBHOOK") in YES_CHARS
    reset_webhook = os.getenv("TELEGRAM_RESET_WEBHOOK") in YES_CHARS
    webhook_path = os.getenv("TELEGRAM_WEBHOOK_PATH")
    webhook_secret = os.getenv("TELEGRAM_WEBHOOK_SECRET")

    return TelegramConfig(
        bot_father_token=bot_father_token,
        drop_pending_updates=drop_pending_updates,
        use_webhook=use_webhook,
        reset_webhook=reset_webhook,
        webhook_path=webhook_path,
        webhook_secret=webhook_secret,
    )
