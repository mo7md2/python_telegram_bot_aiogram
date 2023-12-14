from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import os


load_dotenv()
token = os.getenv("BOT_TOKEN")
bot = Bot(token=token, parse_mode="html")

dp = Dispatcher(bot)
