from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import os


load_dotenv()
token = os.getenv("BOT_TOKEN")
is_production = os.getenv("IS_PRODUCTION", True) != "False"
bot = Bot(token=token, parse_mode="html")

dp = Dispatcher()
