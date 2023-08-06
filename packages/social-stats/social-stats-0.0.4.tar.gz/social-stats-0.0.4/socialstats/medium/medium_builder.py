import json
from datetime import datetime

import requests

from socialstats.base.proxy_mixin import ProxyMixin
from socialstats.constant import Constant
from socialstats.medium.medium_user import MediumUser


class MediumBuilder(ProxyMixin):
    """Medium stat builder class."""

    user = MediumUser()

    def __init__(self, username: str):
        """Construct builder."""
        self.user.username = username

    def _get_profile_data(self):
        """Get profile data from Medium API."""
        url = Constant.medium_endpoint.format(self.user.username)
        try:
            response = requests.get(url, proxies=self._proxies)
        except Exception:
            raise ValueError('Could not connect to the Medium API')

        text_response = response.text.replace(Constant.json_hijacking_prefix, '')
        json_response = json.loads(text_response)
        if json_response:
            return json_response.get('payload')

    @classmethod
    def _human_readable_date(cls, unix_time: int):
        return datetime.fromtimestamp(unix_time / 1000).strftime("%B %d, %Y")

    def _set_posts(self, raw_posts):
        """Set all posts of the user."""
        posts = []
        for k, v in raw_posts.items():
            post = {
                'id': v.get('id'),
                'title': v.get('title'),
                'created_at': v.get('createdAt'),
                'updated_at': v.get('updatedAt'),
                'first_published_at_unix': v.get('firstPublishedAt'),
                'first_published': self._human_readable_date(v.get('firstPublishedAt')),
                'latest_published_at_unix': v.get('latestPublishedAt'),
                'latest_published_at': self._human_readable_date(v.get('latestPublishedAt')),
                'clap_count': v.get('virtuals').get('totalClapCount')
            }
            posts.append(post)

        self.user.posts = posts

    def build_profile(self):
        """Build user basic profile info."""
        user_data = self._get_profile_data()

        if not user_data:
            raise ValueError('No user data found.')
        self.user.id = user_data.get('user').get('userId')
        self.user.first_name = user_data.get('user').get('name')
        self.user.registration_unix_time = user_data.get('user').get('createdAt')
        self.user.image_id = user_data.get('user').get('imageId')
        self.user.bio = user_data.get('user').get('bio')
        self.user.medium_member_at = user_data.get('user').get('mediumMemberAt')
        self.user.language_code = user_data.get('user').get('languageCode')
        self.user.number_of_posts_published = user_data.get('userMeta').get('numberOfPostsPublished')
        self.user.follower = user_data.get('references').get('SocialStats').get(self.user.id).get(
            'usersFollowedByCount')
        self.user.following = user_data.get('references').get('SocialStats').get(self.user.id).get('usersFollowedCount')

        raw_posts = user_data.get('references').get('Post')
        self._set_posts(raw_posts)
        return self

    def return_user(self):
        """Return an instance of user."""
        return self.user
