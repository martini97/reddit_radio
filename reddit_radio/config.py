import configparser
import os

import xdg

PACKAGE_NAME = "reddit_radio"

config = configparser.ConfigParser()
config_file = xdg.xdg_config_home() / PACKAGE_NAME / "config.ini"
config.read(config_file)

REDDIT_CONFIG = {}

if config.has_option("REDDIT", "client_id"):
    REDDIT_CONFIG["client_id"] = config.get("REDDIT", "client_id")

if config.has_option("REDDIT", "client_secret"):
    REDDIT_CONFIG["client_secret"] = config.get("REDDIT", "client_secret")

if config.has_option("REDDIT", "username"):
    REDDIT_CONFIG["username"] = config.get("REDDIT", "username")

if config.has_option("REDDIT", "user_agent"):
    REDDIT_CONFIG["user_agent"] = config.get("REDDIT", "user_agent")

if config.has_option("REDDIT", "subreddits"):
    SUBREDDITS = config.get("REDDIT", "subreddits").split(",")
else:
    SUBREDDITS = []

if config.has_option("DATABASE", "path"):
    DATABASE = config.get("DATABASE", "path")
else:
    DATABASE = xdg.xdg_data_home() / PACKAGE_NAME / "database.db"

if config.has_option("LOGS", "path"):
    LOGS = config.get("LOGS", "path")
else:
    LOGS = xdg.xdg_cache_home() / PACKAGE_NAME / "{time}.log"

if config.has_option("MPV", "path"):
    MPV = config.get("MPV", "path")
else:
    MPV = "mpv"

# NOTE: override stuff for local testing, could not find a proper way to mock
# this on the tests
if os.environ.get("PYTHON_ENV") == "test":
    import tempfile

    DATABASE = tempfile.NamedTemporaryFile().name
