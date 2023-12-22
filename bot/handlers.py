from aiogram import types
from bot.loader import bot, dp
from bot.texts import button_texts, message_texts
from bot.utils import download_youtube
import os


@dp.message_handler(commands="start")
async def start_message(message: types.Message) -> None:
    """welcome message."""
    first_name = message.from_user.first_name
    username = message.from_user.username
    last_name = message.from_user.last_name
    name = first_name or username or last_name or ""
    await bot.send_message(message.chat.id, f"مرحبا {first_name} , \n{message_texts['start']}")


@dp.message_handler(commands=("help", "info", "about"))
async def give_info(message: types.Message) -> None:
    """the target of this bot."""
    await bot.send_message(message.chat.id, message_texts["about"])


@dp.message_handler(commands="contacts")
async def give_contacts(message: types.Message) -> None:
    """ссылка на код проекта."""
    btn_link = types.InlineKeyboardButton(
        text=button_texts["github"], url="https://github.com/donBarbos/telegram-bot-template"
    )
    keyboard_link = types.InlineKeyboardMarkup().add(btn_link)
    await bot.send_message(
        message.chat.id,
        message_texts["github"],
        reply_markup=keyboard_link,
    )


@dp.callback_query_handler(lambda c: c.data == "name")
async def alter_name(callback_query: types.CallbackQuery) -> None:
    await bot.send_message(callback_query.id, message_texts["address"])
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == "lang")
async def alter_lang(callback_query: types.CallbackQuery) -> None:
    await bot.send_message(callback_query.id, message_texts["language"])
    await bot.answer_callback_query(callback_query.id, message_texts["language"])


@dp.message_handler(content_types="text")
async def text_handler(message: types.Message) -> None:
    start_message_text = message_texts["download_started"]
    end_message_text = message_texts["download_ended"]
    url = message.text
    # test url
    if "youtube" in url:
        start_message = await bot.send_message(message.chat.id, start_message_text)
        result = download_youtube(url)
        for res in result:
            if res["status"] == "start":
                text = f"{start_message_text}\n" + f"({res['data']}mb)"
                await start_message.edit_text(text)
            elif res["status"] == "end":
                # await start_message.edit_text(end_message_text)
                path = res["data"]
                video = open(path, "rb")
                await bot.send_video(message.chat.id, video)
                await start_message.edit_text(end_message_text)
                await start_message.delete()
                os.remove(path)
    else:
        await bot.send_message(message.chat.id, "رابط غير معروف")

    # await bot.send_video(message.chat.id, message_texts["text"])


@dp.message_handler()
async def unknown_message(message: types.Message) -> None:
    if not message.is_command():
        await bot.send_message(message.chat.id, message_texts["format_error"])
    else:
        await message.answer(message_texts["command_error"])
