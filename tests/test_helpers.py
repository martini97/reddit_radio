import os

import pytest

from reddit_radio.helpers import fromtimestamp, is_binary, safe_parse


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


class TestIsBinary:
    @pytest.fixture
    def mocked_isfile(self, mocker):
        return mocker.patch("os.path.isfile")

    @pytest.fixture
    def mocked_access(self, mocker):
        return mocker.patch("os.access")

    @pytest.fixture
    def mocked_which(self, mocker):
        return mocker.patch("shutil.which")

    def test_true_if_path_and_executable(self, mocked_isfile, mocked_access, faker):
        mocked_isfile.return_value = True
        mocked_access.return_value = True
        filename = faker.file_path(depth=3)

        assert is_binary(filename)

        mocked_isfile.assert_called_once_with(filename)
        mocked_access.assert_called_once_with(filename, os.X_OK)

    def test_false_if_path_and_not_executable(
        self, mocked_isfile, mocked_access, faker
    ):
        mocked_isfile.return_value = True
        mocked_access.return_value = False
        filename = faker.file_path(depth=3)

        assert not is_binary(filename)

        mocked_isfile.assert_called_once_with(filename)
        mocked_access.assert_called_once_with(filename, os.X_OK)

    def test_false_if_path_and_not_exist(self, mocked_isfile, mocked_access, faker):
        mocked_isfile.return_value = False
        mocked_access.return_value = True
        filename = faker.file_path(depth=3)

        assert not is_binary(filename)

        assert not mocked_access.called
        mocked_isfile.assert_called_once_with(filename)

    def test_true_if_command_and_exist(self, mocked_which, faker):
        mocked_which.return_value = True
        filename = faker.file_name()

        assert is_binary(filename)

        mocked_which.assert_called_once_with(filename)

    def test_false_if_command_and_not_exist(self, mocked_which, faker):
        mocked_which.return_value = False
        filename = faker.file_name()

        assert not is_binary(filename)

        mocked_which.assert_called_once_with(filename)
