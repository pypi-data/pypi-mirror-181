from socialstats.base.user import BaseUser


class CodeChefUser(BaseUser):
    """Codechef user model."""

    motto: str = ''
    avatar_url: str = ''
    org: str = ''
    country: str = ''
    rating: int = 0
    profession: str = ''
    highest_rating: int = 0
    star: int = 0
    solved: int = 0
    authored: int = 0
    tested: int = 0
    contributed: int = 0
