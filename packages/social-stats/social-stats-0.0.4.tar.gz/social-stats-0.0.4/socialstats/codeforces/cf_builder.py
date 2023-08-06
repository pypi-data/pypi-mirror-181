from collections import defaultdict

import requests

from socialstats.base.proxy_mixin import ProxyMixin
from socialstats.codeforces.cf_user import CFUser
from socialstats.constant import Constant


class CFBuilder(ProxyMixin):
    """Codeforces builder class."""

    user = CFUser()

    def __init__(self, username):
        """Construct builder."""
        self.user.username = username

    def _get_user_info(self):
        """Get data from codeforces user.info api."""
        url = Constant.cf_user_info.format(self.user.username)
        try:
            response = requests.get(url, proxies=self._proxies)
        except Exception:
            raise ValueError('Could not connect to the codeforces API')
        return response.json().get('result')[0]

    def _get_user_sub(self):
        """Get data from codeforces user.status api."""
        url = Constant.cf_user_status.format(self.user.username)
        try:
            response = requests.get(url, proxies=self._proxies)
        except Exception:
            raise ValueError('Could not connect to the codeforces API')
        return response.json().get('result')

    def _get_rating_changes(self):
        """Get all rating changes from codeforces api."""
        url = Constant.cf_user_rating.format(self.user.username)
        try:
            response = requests.get(url, proxies=self._proxies)
        except Exception:
            raise ValueError('Could not connect to the codeforces API')
        return response.json().get('result')

    def build_user_info(self):
        """Build user info part."""
        user_info = self._get_user_info()
        self.user.first_name = user_info.get('firstName', '')
        self.user.last_name = user_info.get('lastName', '')
        self.user.org = user_info.get('organization', '')
        self.user.rating = user_info.get('rating', 0)
        self.user.rank = user_info.get('rank', 'newbie')
        self.user.max_rating = user_info.get('maxRating', 0)
        self.user.max_rank = user_info.get('maxRank', 'newbie')
        self.user.contributions = user_info.get('contribution', 0)
        self.user.registration_unix_time = user_info.get('registrationTimeSeconds', 0)
        return self

    def build_user_submission(self):
        """Build user submission detail part."""
        user_submission = self._get_user_sub()
        self.user.submissions = len(user_submission)
        freq: dict = defaultdict(lambda: 0)
        for sb in user_submission:
            freq[sb['verdict']] += 1

        self.user.accepted = freq['OK']
        self.user.wrong_ans = freq['WRONG_ANSWER']
        self.user.tle = freq['TIME_LIMIT_EXCEEDED']
        return self

    def build_rating_changes(self):
        """Set total number of contests participated by the user."""
        rating_changes = self._get_rating_changes()
        self.user.contests = len(rating_changes)
        return self

    def return_user(self):
        """Return an instance of user."""
        return self.user
