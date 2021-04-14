from itertools import chain

import click

from reddit_radio import config
from reddit_radio.database import RedditPost, create_tables_if_needed
from reddit_radio.logging import logger
from reddit_radio.mpv import play
from reddit_radio.reddit import client


def load_data(limit):
    for subreddit in config.SUBREDDITS:
        hot = client.get_pages(subreddit, "hot", limit=limit)
        top = client.get_pages(
            subreddit, "top", time_filter="all", pages=5, limit=limit
        )
        for post in chain.from_iterable([hot, top]):
            RedditPost.get_or_create(reddit_id=post["reddit_id"], defaults=post)


@click.command()
@click.option("--limit", default=100, help="Limit of posts per page")
@click.option("--count", default=100, help="Limit of links in the playlist")
@click.option("--init-db", default=False, help="Create database", is_flag=True)
@click.option("--delete-db", default=False, help="Delete database", is_flag=True)
@click.option(
    "--no-load-data",
    default=False,
    help="Use data from database without refresh",
    is_flag=True,
)
@click.option("--no-play", default=False, help="Don't play", is_flag=True)
def reddit_radio(limit, count, init_db, delete_db, no_load_data, no_play):
    if init_db:
        create_tables_if_needed()

    if delete_db:
        raise NotImplementedError()

    if not no_load_data:
        load_data(limit)

    if not no_play:
        play(count)


if __name__ == "__main__":
    reddit_radio()
