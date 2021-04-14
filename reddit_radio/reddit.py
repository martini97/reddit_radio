import praw

from reddit_radio import config, youtube
from reddit_radio.helpers import fromtimestamp, safe_parse
from reddit_radio.logging import logger


class Client:
    def __init__(self, reddit):
        self.reddit = reddit

    @staticmethod
    def serialize(post):
        return {
            "reddit_id": safe_parse(str, post.fullname, ""),
            "youtube_id": youtube.extract_video_id(post.url),
            "title": safe_parse(str, post.title, ""),
            "url": safe_parse(str, post.url, ""),
            "subreddit": safe_parse(str, post.subreddit.name, ""),
            "upvote_count": safe_parse(int, post.ups, 0),
            "upvote_ratio": safe_parse(int, post.upvote_ratio, 0),
            "submitted_at": fromtimestamp(post.created),
        }

    def get_posts(self, subreddit, method, **params):
        sub = self.reddit.subreddit(subreddit)

        try:
            args = []
            limit = params.pop("limit", 100)

            # walrus is causing black to break here
            # fmt: off
            if (time_filter := params.pop("time_filter", None)):
                args.append(time_filter)
            # fmt: on

            return list(getattr(sub, method)(*args, limit=limit, params=params))
        except Exception:
            logger.exception(f"Failed to get posts from [{subreddit}] with [{method}]")
            return []

    def get_pages(self, subreddit, method, pages=10, **params):
        for page in range(pages):
            posts = self.get_posts(subreddit, method, **params)

            if (posts_count := len(posts)) == 0 or (
                "limit" in params and params["limit"] > posts_count
            ):
                logger.info(f"{subreddit}: reached final page at [{page + 1}]")
                break

            for post in posts:
                yield self.serialize(post)

            logger.info(f"{subreddit}: {page+1:02}/{pages}")

            if (latest := posts[len(posts) - 1]) and latest.fullname:
                params["after"] = latest.fullname
            else:
                logger.info(f"{subreddit}: reached final page at [{page + 1}]")
                break


reddit = praw.Reddit(**config.REDDIT_CONFIG)
client = Client(reddit)
