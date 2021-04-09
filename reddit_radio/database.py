from datetime import datetime

import peewee

from reddit_radio import config

database = peewee.SqliteDatabase(config.DATABASE)


class BaseModel(peewee.Model):
    created_at = peewee.DateTimeField(default=datetime.now)

    class Meta:
        database = database


class RedditPost(BaseModel):
    reddit_id = peewee.CharField(unique=True)
    youtube_id = peewee.CharField(null=True)
    title = peewee.CharField()
    url = peewee.CharField(null=True)
    subreddit = peewee.CharField()
    upvote_count = peewee.IntegerField()
    upvote_ratio = peewee.FloatField()
    submitted_at = peewee.DateTimeField(null=True)

    @classmethod
    def playlist(cls, count=100):
        return (
            cls.select(cls.url)
            .where(cls.youtube_id.is_null(False) & cls.url.is_null(False))
            .limit(count)
            .order_by(peewee.fn.Random())
        )


_tables = [RedditPost]


def create_tables_if_needed():
    if len(database.get_tables()) == len(_tables):
        return

    with database:
        database.create_tables(_tables)
