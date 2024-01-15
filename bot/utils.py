from typing import BinaryIO, List
from pytube import YouTube
from pytube import Stream
from bot.models import Job


def get_youtube_download_options(url: str) -> Job:
    yt = YouTube(url)

    thumbnail_url = yt.thumbnail_url
    video_id = yt.video_id
    audio_stream = yt.streams.filter(mime_type="audio/mp4").first()
    title = yt.title
    video_streams = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc()[:3]
    streams: List[Stream] = [audio_stream] + video_streams
    data = Job(url_msg_id=None, thumbnail_url=thumbnail_url, streams=streams, title=title, video_id=video_id)
    return data


def get_youtube_stream_text(stream):
    res = stream.resolution
    size = stream.filesize_mb
    m_type = stream.mime_type
    text = ""
    if "audio" in m_type:
        text = f"🎤 صوت"
    else:
        text = f"🎥 فيديو {res}"
    return text
