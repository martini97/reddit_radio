import pytest

from reddit_radio.reddit import Client


@pytest.fixture
def mocked_client_subreddit(mocker):
    return mocker.MagicMock()


@pytest.fixture
def mocked_client(mocker, mocked_client_subreddit):
    client = Client()
    mocker.patch.object(client, "_reddit")
    client._reddit.subreddit.return_value = mocked_client_subreddit
    return client


class TestSerialize:
    def test_serializes_post(self, mocked_client, mocker, faker):
        created = faker.date_time()
        post = mocker.MagicMock(
            fullname=faker.pystr(),
            url=faker.url(),
            title=faker.sentence(nb_words=3),
            ups=faker.pyint(),
            upvote_ratio=faker.pyfloat(min_value=0, max_value=1),
            created=created.timestamp(),
        )
        post.subreddit.name = faker.pystr()
        assert mocked_client.serialize(post) == {
            "reddit_id": post.fullname,
            "youtube_id": None,
            "title": post.title,
            "url": post.url,
            "upvote_count": post.ups,
            "upvote_ratio": post.upvote_ratio,
            "submitted_at": created.isoformat(),
            "subreddit": post.subreddit.name,
        }


class TestGetPosts:
    def test_handles_time_filter(self, mocked_client, mocked_client_subreddit, faker):
        subreddit = faker.pystr()
        mocked_client.get_posts(subreddit, "all", time_filter="month")
        mocked_client_subreddit.all.assert_called_once_with(
            "month", limit=100, params={}
        )

    def test_handles_limit(self, mocked_client, mocked_client_subreddit, faker):
        subreddit = faker.pystr()
        limit = faker.pyint()
        mocked_client.get_posts(subreddit, "hot", limit=limit)
        mocked_client_subreddit.hot.assert_called_once_with(limit=limit, params={})

    def test_returns_list_from_generator(
        self, mocked_client, mocked_client_subreddit, faker
    ):
        subreddit = faker.pystr()
        limit = faker.pyint()
        generator = (i for i in range(10))
        mocked_client_subreddit.hot.return_value = generator

        assert mocked_client.get_posts(subreddit, "hot", limit=limit) == list(range(10))

    def test_returns_empty_list_if_error(
        self, mocked_client, mocked_client_subreddit, faker
    ):
        subreddit = faker.pystr()
        limit = faker.pyint()
        mocked_client_subreddit.hot.side_effect = Exception

        assert mocked_client.get_posts(subreddit, "hot", limit=limit) == []
