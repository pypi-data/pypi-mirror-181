from socialstats.base.user import BaseUser


class StackUser(BaseUser):
    """Stackoverflow user class."""

    badge_bronze: int = 0
    badge_silver: int = 0
    badge_gold: int = 0
    is_employee: bool = False
    location: str = ''
    website_url: str = ''
    avatar_url: str = ''
    profile_link: str = ''
    registration_date: int = 0
    reputation: int = 0
    acc_rate: int = 0
