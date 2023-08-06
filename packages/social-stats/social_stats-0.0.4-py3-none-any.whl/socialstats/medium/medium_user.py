from typing import List

from socialstats.base.user import BaseUser


class MediumUser(BaseUser):
    """Medium user class."""

    id: str = ''
    image_id: str = ''
    bio: str = ''
    medium_member_at: int = 0
    registration_unix_time: int = 0
    follower: int = 0
    following: int = 0
    number_of_posts_published: int = 0
    language_code: str = ''
    posts: List = []

    @property
    def top_posts(self, limit: int = 5):
        """Return the rating color."""
        return sorted(self.posts, key=lambda d: d.get('latest_published_at_unix'))

