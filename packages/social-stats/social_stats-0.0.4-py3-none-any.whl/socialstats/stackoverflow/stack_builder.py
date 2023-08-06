import requests

from socialstats.base.proxy_mixin import ProxyMixin
from socialstats.constant import Constant
from socialstats.stackoverflow.stack_user import StackUser


class StackOverflowBuilder(ProxyMixin):
    """StackOverflow stat builder class."""

    user = StackUser()

    def __init__(self, username: str, key: str):
        """Construct builder."""
        self.user.username = username
        self.key = key

    def _get_profile_data(self):
        """Get profile data from stackoverflow API."""
        url = Constant.stack_overflow_endpoint.format(self.user.username)
        params = {'key': self.key}
        try:
            response = requests.get(url, params=params, proxies=self._proxies)
        except Exception:
            raise ValueError('Could not connect to the stackoverflow API')
        data_arr = response.json().get('items')
        if data_arr:
            return data_arr[0]

    def build_profile(self):
        """Build user basic profile info."""
        user_data = self._get_profile_data()
        if not user_data:
            raise ValueError('No user data found.')
        badge_counts = user_data.get('badge_counts')
        self.user.first_name = user_data.get('display_name')
        self.user.badge_bronze = badge_counts.get('bronze')
        self.user.badge_silver = badge_counts.get('silver')
        self.user.badge_gold = badge_counts.get('gold')
        self.user.is_employee = user_data.get('is_employee')
        self.user.registration_date = user_data.get('creation_date')
        self.user.location = user_data.get('location')
        self.user.website_url = user_data.get('website_url')
        self.user.profile_link = user_data.get('link')
        self.user.avatar_url = user_data.get('profile_image')
        self.user.acc_rate = user_data.get('accept_rate')

        return self

    def return_user(self):
        """Return an instance of user."""
        return self.user
