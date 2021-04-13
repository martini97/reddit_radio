import subprocess

from reddit_radio.config import MPV
from reddit_radio.database import RedditPost
from reddit_radio.helpers import cache_file
from reddit_radio.logging import logger


def get_playlist(count):
    playlist = [u.url for u in RedditPost.playlist(count)]
    return playlist


def save_playlist(playlist):
    file = cache_file("reddit-radio-playlist.txt")
    file.write_text("\n".join(playlist))
    return str(file)


def build_cmd(file):
    return [
        MPV,
        "--input-ipc-server=/tmp/mpvsocket",
        "--no-video",
        f"--playlist={file}",
    ]


def play(count):
    playlist = get_playlist(count)
    file = save_playlist(playlist)
    logger.info(f"Playing playlist [{file}]")
    process = subprocess.Popen(
        build_cmd(file), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    logger.info(f"Started mpv with PID [{process.pid}]")
    return process.pid
