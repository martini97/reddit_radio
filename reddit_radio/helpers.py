import os
import shutil
from datetime import datetime

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


def is_binary(filename):
    fpath, fname = os.path.split(filename)
    if not fpath:
        return bool(shutil.which(fname))
    return os.path.isfile(filename) and os.access(filename, os.X_OK)


class SingletonMeta(type):
    """
    From https://refactoring.guru/design-patterns/singleton/python/example
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
