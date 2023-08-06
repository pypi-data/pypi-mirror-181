from socialstats.base.user import BaseUser


class TwitterUser(BaseUser):
    """Twitter user class."""

    followers_count: int = 0
    following_count: int = 0
    tweet_count: int = 0
    listed_count: int = 0
    id: int = 0
