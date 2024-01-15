from aiogram import types, Bot


async def set_default_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        commands=[
            types.BotCommand(command="about", description="نحن"),
            # types.BotCommand("contacts", "developer contact details"),
            # types.BotCommand("settings", "setting information about you"),
        ]
    )
