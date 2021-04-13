import re
from pathlib import Path

import pytest
from xdg import xdg_cache_home

from reddit_radio import config
from reddit_radio.helpers import cache_file, fromtimestamp, safe_parse


def throws(_):
    raise Exception()


@pytest.fixture(autouse=True)
def mocked_logger(mocker):
    return mocker.patch("reddit_radio.helpers.logger")


@pytest.fixture(autouse=True)
def mocked_mkdir(mocker):
    return mocker.patch("pathlib.Path.mkdir")


class TestSafeParse:
    def test_logs_exception(self, faker, mocked_logger):
        value = faker.pyint()
        safe_parse(throws, value)
        mocked_logger.exception.assert_called_once_with(f"Failed to parse [{value}]")

    def test_returns_fallback_if_error(self, faker):
        value = faker.pyint()
        fallback = faker.pystr()
        result = safe_parse(throws, value, fallback)
        assert result == fallback

    def return_parsed_value_if_ok(self, faker):
        value = faker.pyint()
        result = safe_parse(int, str(value))
        assert result == value


class TestFromtimestamp:
    def test_parse_timestamp(self, faker):
        value = faker.date_time()
        assert fromtimestamp(value.timestamp()) == value.isoformat()

    def test_logs_exception(self, faker, mocked_logger):
        value = faker.pystr()
        fromtimestamp(value)
        mocked_logger.exception.assert_called_once_with(f"Failed to parse [{value}]")
        mocked_logger.warning.assert_called_once_with(
            f"Failed to get datetime from timestamp [{value}]"
        )

    def test_returns_none_if_failed(self, faker):
        value = faker.pystr()
        assert fromtimestamp(value) is None


class TestCacheFile:
    def test_returns_file(self, faker):
        value = faker.pystr()
        file = cache_file(value)
        parent, filename = file.relative_to(xdg_cache_home()).parts
        match = re.search(r"^\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}-(.*)", filename)
        assert isinstance(file, Path)
        assert parent == config.PACKAGE_NAME
        assert match is not None
        assert match.groups()[0] == value

    def test_creates_parents(self, faker, mocked_mkdir):
        cache_file(faker.pystr())
        mocked_mkdir.assert_called_once_with(parents=True, exist_ok=True)
