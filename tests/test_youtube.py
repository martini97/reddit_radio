import pytest

from reddit_radio.youtube import extract_video_id

youtube_urls = [
    "https://www.youtube.com/watch?v=0zM3nApSvMg&feature=feedrec_grec_index",
    "https://www.youtube.com/v/0zM3nApSvMg?fs=1&amp;hl=en_US&amp;rel=0",
    "https://www.youtube.com/watch?v=0zM3nApSvMg#t=0m10s",
    "https://www.youtube.com/embed/0zM3nApSvMg?rel=0",
    "https://www.youtube.com/watch?v=0zM3nApSvMg",
    "https://youtu.be/0zM3nApSvMg",
    (
        "https://www.youtube.com/attribution_link?a=PUSfls4FSYQ&u"
        "=%2Fwatch%3Fv%3D0zM3nApSvMg%26feature%3Dshare"
    ),
    "https://www.youtube.com/playlist?list=0zM3nApSvMg",
    "www.youtube.com/watch?v=0zM3nApSvMg&feature=feedrec_grec_index",
    "www.youtube.com/v/0zM3nApSvMg?fs=1&amp;hl=en_US&amp;rel=0",
    "www.youtube.com/watch?v=0zM3nApSvMg#t=0m10s",
    "www.youtube.com/embed/0zM3nApSvMg?rel=0",
    "www.youtube.com/watch?v=0zM3nApSvMg",
    "youtu.be/0zM3nApSvMg",
    "www.youtube.com/attribution_link?a=PUSfls4FSYQ&u=%2Fwatch%3Fv%3D0zM3nApSvMg%26feature%3Dshare",
    "www.youtube.com/playlist?list=0zM3nApSvMg",
    "https://music.youtube.com/watch?v=0zM3nApSvMg&feature=share",
    "https://m.youtube.com/watch?v=0zM3nApSvMg",
]


@pytest.mark.parametrize("url", youtube_urls)
def test_gets_expected_id(url):
    assert extract_video_id(url) == "0zM3nApSvMg"


def test_none_if_non_youtube_id(faker):
    assert extract_video_id(faker.url()) is None


def test_none_if_youtube_but_no_id():
    assert extract_video_id("www.youtube.com") is None
