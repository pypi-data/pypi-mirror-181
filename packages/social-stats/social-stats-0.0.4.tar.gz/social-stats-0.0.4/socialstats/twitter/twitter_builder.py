import requests

from socialstats.base.proxy_mixin import ProxyMixin
from socialstats.constant import Constant
from socialstats.twitter.twitter_user import TwitterUser


class TwitterBuilder(ProxyMixin):
    """Twitter stat builder class."""

    user = TwitterUser()

    def __init__(self, username: str, token: str):
        """Construct builder."""
        self.user.username = username
        self.token = token

    def _get_profile_data(self):
        """Get profile data from Twitter API."""
        url = Constant.twitter_endpoint.format(self.user.username)
        headers = {'Authorization': 'Bearer ' + self.token}
        try:
            response = requests.get(url, headers=headers, proxies=self._proxies)
        except Exception:
            raise ValueError('Could not connect to the stackoverflow API')
        json_res = response.json()
        if json_res:
            return json_res.get('data')

    def build_profile(self):
        """Build user basic profile info."""
        user_data = self._get_profile_data()
        if not user_data:
            raise ValueError('No user data found.')
        self.user.first_name = user_data.get('name')
        self.user.id = user_data.get('id')
        self.user.followers_count = user_data.get('public_metrics').get('followers_count')
        self.user.following_count = user_data.get('public_metrics').get('following_count')
        self.user.tweet_count = user_data.get('public_metrics').get('tweet_count')
        self.user.listed_count = user_data.get('public_metrics').get('listed_count')

        return self

    def return_user(self):
        """Return an instance of user."""
        return self.user
