from datetime import datetime

from xdg import xdg_cache_home

from reddit_radio import config
from reddit_radio.logging import logger


def safe_parse(parser, value, fallback=None):
    try:
        return parser(value)
    except Exception:
        logger.exception(f"Failed to parse [{value}]")
        return fallback


def fromtimestamp(timestamp):
    dt = safe_parse(datetime.fromtimestamp, timestamp)
    if not dt:
        logger.warning(f"Failed to get datetime from timestamp [{timestamp}]")
        return None
    return dt.isoformat()


def cache_file(filename):
    date_string = datetime.now().isoformat(timespec="seconds").replace(":", "-")
    cache_filename = f"{date_string}-{filename}"
    cache_dir = xdg_cache_home() / config.PACKAGE_NAME
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / cache_filename
