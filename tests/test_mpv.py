import pytest
from click.exceptions import UsageError
from mixer.backend.peewee import mixer

from reddit_radio.database import RedditPost
from reddit_radio.mpv import Client


@pytest.fixture(autouse=True)
def mocked_mpv(mocker):
    return mocker.patch("reddit_radio.mpv.MPVClient")


@pytest.fixture
def mocked_client(mocker):
    client = Client()
    mocker.patch.object(client, "_client")
    return client


@pytest.fixture
def playlist(faker):
    count = faker.pyint(min_value=2, max_value=10)
    playlist = mixer.cycle(count).blend(
        RedditPost, url=faker.url(), youtube_id=faker.pystr()
    )
    return playlist


@pytest.fixture
def mocked_is_binary(mocker):
    return mocker.patch("reddit_radio.mpv.is_binary")


def test_check_for_binary(mocked_is_binary):
    mocked_is_binary.return_value = False

    with pytest.raises(UsageError):
        Client()


def test_loads_playlist(playlist, mocked_client):
    mocked_client.load_playlist(len(playlist))
    for track in playlist:
        mocked_client._client.loadfile.assert_called_with(track.url, "append")


def test_play_with_playlist_not_started(mocked_client):
    mocked_client._client.playlist_current_pos = -1
    mocked_client.play()
    mocked_client._client.playlist_play_index.assert_called_once_with(0)


def test_play_with_playlist_started(mocked_client, faker):
    current_pos = faker.pyint(min_value=1, max_value=10)
    mocked_client._client.playlist_current_pos = current_pos
    mocked_client.play()
    mocked_client._client.playlist_play_index.assert_called_once_with(current_pos)


def test_playlist(playlist, mocked_client, faker):
    current_pos = faker.pyint(min_value=1, max_value=len(playlist))
    mocked_client._client.playlist_current_pos = current_pos

    mocked_client.playlist(len(playlist))

    for track in playlist:
        mocked_client._client.loadfile.assert_called_with(track.url, "append")
    mocked_client._client.playlist_play_index.assert_called_once_with(current_pos)
