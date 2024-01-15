from aiogram import Dispatcher, Bot
from bot.commands import set_default_commands
from bot.loader import bot, dp, is_production
from loguru import logger
from bot.keep_alive import keep_alive
import asyncio


async def on_startup(bot: Bot) -> None:
    """initialization"""
    await set_default_commands(bot)
    logger.info("bot started")


async def shutdown() -> None:
    """fi there is need to close the connection when shutdown"""
    logger.info("bot finished")


async def main() -> None:
    # And the run events dispatching
    dp.startup.register(on_startup)
    dp.shutdown.register(shutdown)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.add(
        "logs/debug.log",
        level="DEBUG",
        format="{time} | {level} | {module}:{function}:{line} | {message}",
        rotation="30 KB",
        compression="zip",
    )

    if is_production:
        keep_alive()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Program interrupted. Stopping gracefully...")
