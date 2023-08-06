from socialstats.base.user import BaseUser


class LeetUser(BaseUser):
    """Leetcode user class."""

    about: str = ''
    avatar_url: str = ''
    skills: list = []
    country: str = ''
    ranking: int = 0
    submission: int = 0
    easy: int = 0
    medium: int = 0
    hard: int = 0
    contest_rating: float = 0
    contest_rank: int = 0
    badge: str = ''
