from aiogram import Dispatcher, types


async def set_default_commands(dp: Dispatcher) -> None:
    await dp.bot.set_my_commands(
        [
            types.BotCommand("help", "مساعدة"),
            # types.BotCommand("contacts", "developer contact details"),
            # types.BotCommand("settings", "setting information about you"),
        ]
    )
