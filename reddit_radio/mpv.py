from click.exceptions import UsageError
from python_mpv_jsonipc import MPV as MPVClient

from reddit_radio.config import COOKIES_FILE
from reddit_radio.config import MPV as MPV_BIN
from reddit_radio.database import RedditPost
from reddit_radio.helpers import SingletonMeta, is_binary
from reddit_radio.logging import logger


class Client(metaclass=SingletonMeta):
    def __init__(self):
        Client.check_mpv()

        kwargs = {}
        if COOKIES_FILE:
            kwargs["cookies"] = True
            kwargs["cookies_file"] = str(COOKIES_FILE)
            kwargs["ytdl_raw_options"] = f"cookies={COOKIES_FILE}"

        self._client = MPVClient(
            input_terminal=True,
            ipc_socket="/tmp/mpvsocket",
            mpv_location=MPV_BIN,
            start_mpv=True,
            terminal=True,
            video=False,
            **kwargs,
        )

    @staticmethod
    def check_mpv():
        if not is_binary(MPV_BIN):
            logger.error("mpv binary not found.")
            raise UsageError("mpv binary not found.")

    def load_playlist(self, count):
        for track in RedditPost.playlist(count):
            self._client.loadfile(track.url, "append")

    def play(self):
        index = index if (index := self._client.playlist_current_pos) >= 0 else 0
        self._client.playlist_play_index(index)

    def playlist(self, count):
        self.load_playlist(count)
        self.play()
