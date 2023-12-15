from pytube import YouTube
from typing import BinaryIO


def download_youtube(url: str):
    stream = YouTube(url).streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
    size = {"status": "start", "data": stream.filesize_mb}

    yield size
    path = stream.download()
    yield {"status": "end", "data": path}


def on_yt_progress(chunk: bytes, file_handler: BinaryIO, bytes_remaining: int, size: int) -> None:
    print(f"downloaded ({size/bytes_remaining})")
