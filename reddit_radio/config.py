import configparser
import os

import xdg


class Config:
    def __init__(self, config_file):
        self._config_file = config_file
        self._config = configparser.ConfigParser()
        self._config.read(self._config_file)

    def get(self, section, option, fallback=None):
        if self._config.has_option(section, option):
            return self._config.get(section, option)
        return fallback


PACKAGE_NAME = "reddit_radio"

config = Config(xdg.xdg_config_home() / PACKAGE_NAME / "config.ini")

REDDIT_CONFIG = {
    "client_id": config.get("REDDIT", "client_id", ""),
    "client_secret": config.get("REDDIT", "client_secret", ""),
    "username": config.get("REDDIT", "username", ""),
    "user_agent": config.get("REDDIT", "user_agent", ""),
}
SUBREDDITS = (
    subreddits.split(",") if (subreddits := config.get("REDDIT", "subreddits")) else []
)
DATABASE = config.get(
    "DATABASE", "path", xdg.xdg_data_home() / PACKAGE_NAME / "database.db"
)
LOGS = config.get("LOGS", "path", xdg.xdg_cache_home() / PACKAGE_NAME / "{time}.log")
MPV = config.get("MPV", "path", "mpv")

# NOTE: override stuff for local testing, could not find a proper way to mock
# this on the tests
if os.environ.get("PYTHON_ENV") == "test":
    import tempfile

    DATABASE = tempfile.NamedTemporaryFile().name
