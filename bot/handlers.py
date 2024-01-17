import os
from typing import Any, Dict, List, Optional
from loguru import logger
from aiogram import types
from aiogram.filters import CommandStart, Command, exception
from aiogram.filters.callback_data import CallbackData
from aiogram.types.error_event import ErrorEvent

from bot.loader import bot, dp
from bot.texts import message_texts
from bot.utils import generate_id, get_youtube_download_options, get_youtube_stream_text, YOUTUBE_FILESIZE_LIMIT
from bot.models import Job
from pytube import Stream


class YoutubeCallback(CallbackData, prefix="youtube_download"):
    id: str
    stream_index: int


jobs: Dict[str, Job] = {}


@dp.message(Command("about"))
async def command_about_handler(message: types.Message) -> None:
    """
    This handler receives messages with `/about` command
    """
    repo = "https://github.com/mo7md2/python_telegram_bot_aiogram"
    about_message = (
        "👋مرحبا \n"
        + "تم تطوير هذا البوت ( مفتوح المصدر ) من قبل محمد👨‍💻\n"
        + "ارجو ان ينال على رضاك ويكون مفيد لك \n"
        + "يسعدني استقبال اقتراحاتك على الرقم \n"
        + "0559999682\n"
        + "للمزيد عن البوت وبرمجته تفضل بزيارة المصدر \n"
        + repo
    )
    await message.answer(text=about_message)


@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    first_name = message.from_user.first_name
    await message.answer(text=f"مرحبا {first_name} , \n{message_texts['start']}")


@dp.message()
async def text_handler(message: types.Message) -> None:
    getting_info_text = message_texts["getting_info"]
    unknown_url_text = message_texts["unknown_url"]
    url = message.text
    if "youtu" in url:
        logger.info(f"youtube url is received : {url}")
        try:
            getting_info_msg = await message.reply(getting_info_text)
            data = get_youtube_download_options(url)
            photo_url = data.thumbnail_url
            id = post_job(data=data)
            caption = data.title
            data.url_msg_id = message.message_id
            kb_markup = get_download_options_keyboard(id, data.streams)
            await getting_info_msg.delete()
            await message.reply_photo(photo=photo_url, caption=caption, reply_markup=kb_markup)
        except Exception as e:
            logger.info(f"getting info failed: {url}  - {e}")
            await message.answer(text=message_texts["getting_info_failed"])

    else:
        await message.reply(unknown_url_text)


def get_download_options_keyboard(id: str, streams: List[Stream]):
    btn_list = []
    for index, stream in enumerate(streams):
        callback_data = YoutubeCallback(id=id, stream_index=index).pack()
        text = get_youtube_stream_text(stream)
        btn_list.append([types.InlineKeyboardButton(text=text, callback_data=callback_data)])
    return types.inline_keyboard_markup.InlineKeyboardMarkup(inline_keyboard=btn_list)


# vote_cb.filter(action='up')
@dp.callback_query(YoutubeCallback.filter())
async def download_youtube_cb_handler(query: types.CallbackQuery, callback_data: YoutubeCallback):
    id = callback_data.id
    index = callback_data.stream_index
    job_data = get_job(id)
    try:
        if job_data is None:
            raise Exception("job not found")

        url_msg_id = job_data.url_msg_id
        stream: Stream = job_data.streams[index]
        if stream.filesize_mb >= YOUTUBE_FILESIZE_LIMIT:
            await bot.send_message(chat_id=query.from_user.id, text=message_texts["file_size_limit"])
            return False
        await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
        download_started_msg = await bot.send_message(
            chat_id=query.from_user.id, text=message_texts["download_started"]
        )
        path = stream.download()
        logger.info(f"file is downloaded, path: {path}")

        buffer = types.FSInputFile(path=path, filename=stream.title)
        if "audio" in stream.mime_type:
            await bot.send_audio(chat_id=query.from_user.id, audio=buffer)
        else:
            await bot.send_video(chat_id=query.from_user.id, video=buffer)
        emoji = types.ReactionTypeEmoji(emoji="👍")
        await bot.set_message_reaction(chat_id=query.from_user.id, message_id=url_msg_id, reaction=[emoji])
        # Telegram server says - Bad Request: query is too old and response timeout expired or query ID is invalid
        # await bot.answer_callback_query(callback_query_id=query.id, text=message_texts["download_ended"])
    except Exception as e:
        logger.info(f"downloaded failed: id={id} - {e}")
        await bot.send_message(chat_id=query.from_user.id, text=message_texts["download_failed"])
        emoji = types.ReactionTypeEmoji(emoji="👾")
        await bot.set_message_reaction(chat_id=query.from_user.id, message_id=url_msg_id, reaction=[emoji])

    await download_started_msg.delete()
    os.remove(path)


def get_job(id: str) -> Optional[Job]:
    """
    Retrieve the job associated with the given job ID.

    Args:
        id (str): The ID of the job.

    Returns:
        Optional[Job]: The job associated with the job ID, or None if no job is found.
    """
    return jobs.get(id)


def post_job(data: Job, id: Optional[str] = None) -> Job:
    """
    Save the job data with the given id.

    Args:
        id (str): The ID of the job.
        data (Job): The data to be saved.

    Returns:
        id: The saved ID of the job.
    """
    if id == None or id in jobs:
        return post_job(data, generate_id())
    else:
        jobs[id] = data
        return id
