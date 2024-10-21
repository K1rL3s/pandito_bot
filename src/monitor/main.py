import asyncio
import os
import subprocess

from aiogram import Bot

TELEGRAM_BOT_TOKEN = os.getenv("MONITOR_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("MONITOR_CHAT")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError(
        "MONITOR_TOKEN and MONITOR_CHAT must be set as environment variables",
    )

bot = Bot(token=TELEGRAM_BOT_TOKEN)


async def send_message(text):
    try:
        await bot.send_message(TELEGRAM_CHAT_ID, text)
    except Exception as e:
        print(f"Error sending message: {e}")


async def stream_docker_logs():
    process = subprocess.Popen(
        ["docker", "compose", "logs", "--follow", "--no-color"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    while True:
        output = process.stdout.readline().decode("utf-8")
        if output:
            await send_message(output.strip())
            await asyncio.sleep(0.2)


async def main():
    await stream_docker_logs()


if __name__ == "__main__":
    asyncio.run(main())
