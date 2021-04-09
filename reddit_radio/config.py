import configparser
from pathlib import Path

config = configparser.ConfigParser()

config.read(
    [str(Path.home().joinpath(".config", "reddit_radio.ini")), "data/config.ini"]
)

REDDIT_CONFIG = {
    "client_id": config.get("REDDIT", "client_id"),
    "client_secret": config.get("REDDIT", "client_secret"),
    "username": config.get("REDDIT", "username"),
    "user_agent": config.get("REDDIT", "user_agent"),
}

SUBREDDITS = config.get("REDDIT", "subreddits").split(",")

DATABASE = config.get("DATABASE", "path")
