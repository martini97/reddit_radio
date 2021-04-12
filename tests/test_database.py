import pytest
from mixer.backend.peewee import mixer

from reddit_radio.database import RedditPost, _tables, create_tables_if_needed


@pytest.fixture
def mocked_database(mocker):
    return mocker.patch("reddit_radio.database.database")


class TestCreateTablesIfNeeded:
    def test_create_tables_if_needed(self, mocked_database):
        mocked_database.get_tables.return_value = []
        create_tables_if_needed()
        mocked_database.create_tables.assert_called_once()

    def test_skip_create_tables(self, mocked_database):
        mocked_database.get_tables.return_value = _tables
        create_tables_if_needed()
        assert not mocked_database.create_tables.called


class TestRedditPost:
    def test_playlist_query(self, faker):
        in_playlist = mixer.cycle(5).blend(
            RedditPost, youtube_id=faker.pystr(), url=faker.url()
        )
        mixer.cycle(5).blend(RedditPost, youtube_id=None, url=None)

        playlist = RedditPost.playlist(count=len(in_playlist) + 1)

        assert len(playlist) == len(in_playlist)
        assert {p.url for p in in_playlist} == {p.url for p in playlist}
