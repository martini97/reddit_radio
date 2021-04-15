from itertools import chain
from pathlib import Path

import click

from reddit_radio import config
from reddit_radio.database import RedditPost, create_tables_if_needed
from reddit_radio.mpv import Client as MpvClient
from reddit_radio.reddit import Client as RedditClient


@click.group(chain=True)
def cli():
    pass


@cli.command()
@click.option("--count", default=100, help="Limit of tracks in the playlist")
def play(count):
    mpv = MpvClient()
    mpv.playlist(count)


@cli.command()
@click.option("--limit", default=100, help="Limit of posts per page")
@click.option("--pages", default=5, help="Number of pages to search")
def load_data(limit, pages):
    create_tables_if_needed()
    reddit = RedditClient()

    for post in chain.from_iterable(
        fn(sub, limit=limit, pages=pages)
        for sub in config.SUBREDDITS
        for fn in (reddit.hot, reddit.all)
    ):
        RedditPost.get_or_create(reddit_id=post["reddit_id"], defaults=post)


@cli.command()
@click.option("--force/--no-force", default=False, help="Override config if exists")
def make_config(force):
    config_file = config.config._config_file
    if not force and config_file.exists():
        click.echo("Config file found, skipping...")
        return

    template = Path(__file__).parent / "templates/config.sample.ini"
    config_file.parent.mkdir(exist_ok=True, parents=True)
    config_file.touch()
    config_file.write_text(template.read_text())
    click.echo(
        f"Config file created at {config_file}. Update the values before running."
    )
