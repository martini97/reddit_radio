import pytest
from mixer.backend.peewee import mixer

from reddit_radio import mpv
from reddit_radio.database import RedditPost
from reddit_radio.mpv import build_cmd, get_playlist, play, save_playlist


@pytest.fixture
def playlist(faker):
    count = faker.pyint(min_value=2, max_value=10)
    playlist = mixer.cycle(count).blend(
        RedditPost, url=faker.url(), youtube_id=faker.pystr()
    )
    return playlist


@pytest.fixture(autouse=True)
def mocked_subprocess(mocker):
    return mocker.patch("reddit_radio.mpv.subprocess")


@pytest.fixture(autouse=True)
def mocked_logger(mocker):
    return mocker.patch("reddit_radio.mpv.logger")


class TestGetPlaylist:
    def test_returns_playlist(self, playlist):
        expected = {p.url for p in playlist}

        received = set(get_playlist(len(playlist)))
        assert received == expected


class TestSavePlaylist:
    def test_saves_playlist_to_file(self, playlist, temp_file, mocker):
        mocker.patch("reddit_radio.mpv.cache_file", return_value=temp_file)
        save_playlist(get_playlist(len(playlist)))
        assert temp_file.read_text() == "\n".join(p.url for p in playlist)


class TestBuildCmd:
    def test_build_command(self, faker):
        file = faker.file_name(extension="txt")

        cmd = build_cmd(file)

        assert cmd == [
            "mpv",
            "--input-ipc-server=/tmp/mpvsocket",
            "--no-video",
            f"--playlist={file}",
        ]

    def test_build_command_with_custom_mpv_path(self, faker, mocker):
        mpv_path = faker.file_path(depth=3)
        file = faker.file_name(extension="txt")
        mocker.patch.object(mpv, "MPV", new=mpv_path)

        cmd = build_cmd(file)

        assert cmd == [
            mpv_path,
            "--input-ipc-server=/tmp/mpvsocket",
            "--no-video",
            f"--playlist={file}",
        ]


class TestPlay:
    @pytest.fixture(autouse=True)
    def mocked_save_playlist(self, mocker):
        return mocker.patch(
            "reddit_radio.mpv.save_playlist", return_value="playlist.txt"
        )

    @pytest.fixture(autouse=True)
    def mocked_build_cmd(self, mocker):
        return mocker.patch("reddit_radio.mpv.build_cmd", return_value="command")

    def test_log_playlist_path(self, playlist, mocked_logger):
        play(len(playlist))
        first_call = mocked_logger.info.call_args_list[0][0][0]
        assert first_call == "Playing playlist [playlist.txt]"

    def test_start_command_on_subprocess(self, playlist, mocked_subprocess, mocker):
        play(len(playlist))
        mocked_subprocess.Popen.assert_called_once_with(
            "command", stdout=mocker.ANY, stderr=mocker.ANY
        )

    def test_log_pid(self, playlist, mocked_subprocess, mocked_logger, faker, mocker):
        pid = faker.pyint()
        mocked_subprocess.Popen.return_value = mocker.MagicMock(pid=pid)
        play(len(playlist))
        second_call = mocked_logger.info.call_args_list[1][0][0]
        assert second_call == f"Started mpv with PID [{pid}]"
