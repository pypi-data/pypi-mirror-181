import requests

from socialstats.base.proxy_mixin import ProxyMixin
from socialstats.constant import Constant
from socialstats.leetcode.leet_user import LeetUser


class LeetBuilder(ProxyMixin):
    """Leetcode builder class."""

    user = LeetUser()

    def __init__(self, username: str):
        """Construct builder."""
        self.user.username = username

    def _query_basic_profile(self):
        """Query data from leetcode graphql API."""
        query = {
            'operationName': 'data',
            'variables': {'username': self.user.username},
            'query': """
                query data($username: String!) {
                    user: matchedUser(username: $username) {
                        username
                        profile { 
                            realname: realName 
                            about: aboutMe 
                            avatar: userAvatar 
                            skills: skillTags 
                            country: countryName 
                            ranking
                        }
                    }
            }
            """,
        }
        try:
            response = requests.post(Constant.leetcode_api_endpoint, json=query, proxies=self._proxies)
        except Exception:
            raise ValueError('Could not connect to the leetcode API')
        return response.json().get('data')

    def _query_submissions(self):
        """Query data from leetcode graphql API."""
        query = {
            'operationName': 'data',
            'variables': {'username': self.user.username},
            'query': """
                query data($username: String!) {
                    submissions: matchedUser(username: $username) {
                        submits: submitStats {
                            ac: acSubmissionNum { difficulty count }
                        }
                    }
                }
            """,
        }
        try:
            response = requests.post(Constant.leetcode_api_endpoint, json=query, proxies=self._proxies)
        except Exception:
            raise ValueError('Could not connect to the leetcode API')
        return response.json().get('data')

    def _query_contest_info(self):
        """Query data from leetcode graphql API."""
        query = {
            'operationName': 'data',
            'variables': {'username': self.user.username},
            'query': """
                query data($username: String!) {
                    contest: userContestRanking(username: $username) {
                        rating
                        ranking: globalRanking
                        badge {
                            name
                        }
                    }
                }
            """,
        }
        try:
            response = requests.post(Constant.leetcode_api_endpoint, json=query, proxies=self._proxies)
        except Exception:
            raise ValueError('Could not connect to the leetcode API')
        return response.json().get('data')

    def build_basic_profile(self):
        """Build user basic profile info."""
        user_data = self._query_basic_profile().get('user')
        if not user_data:
            raise ValueError('No user data found.')
        profile = user_data.get('profile')
        self.user.first_name = profile.get('realname')
        self.user.about = profile.get('about')
        self.user.avatar_url = profile.get('avatar')
        self.user.skills = profile.get('skills')
        self.user.country = profile.get('country')
        self.user.ranking = profile.get('ranking')

        return self

    def build_submission_info(self):
        """Build user submission info."""
        submissions = self._query_submissions().get('submissions')
        if not submissions:
            raise ValueError('No user data found.')

        acc_sub = submissions.get('submits').get('ac')
        for sub_data in acc_sub:  # NOQA: WPS110
            if sub_data.get('difficulty') == 'All':
                self.user.submission = sub_data.get('count')
            elif sub_data.get('difficulty') == 'Easy':
                self.user.easy = sub_data.get('count')
            elif sub_data.get('difficulty') == 'Medium':
                self.user.medium = sub_data.get('count')
            elif sub_data.get('difficulty') == 'Hard':
                self.user.hard = sub_data.get('count')

        return self

    def build_contest_info(self):
        """Build user contest info."""
        contest = self._query_contest_info().get('contest')
        if not contest:
            raise ValueError('No user data found.')

        self.user.contest_rating = contest.get('rating')
        self.user.contest_rank = contest.get('ranking')
        self.user.badge = contest.get('badge', '')

        return self

    def return_user(self):
        """Return an instance of user."""
        return self.user
