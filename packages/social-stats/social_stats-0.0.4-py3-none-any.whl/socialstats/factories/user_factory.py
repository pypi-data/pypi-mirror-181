from socialstats.codechef.cc_director import CodeChefDirector
from socialstats.codeforces.cf_director import CFDirector
from socialstats.constant import Constant
from socialstats.leetcode.leet_director import LeetDirector
from socialstats.medium.medium_director import MediumDirector
from socialstats.stackoverflow.stack_director import StackOverflowDirector
from socialstats.twitter.twitter_director import TwitterDirector


class UserFactory:
    """Builds user."""

    @classmethod
    def create_user(cls, platform: str, username: str, token: str = '', proxy: str = ''):
        """Return expected user according to the platform."""
        if platform == Constant.available_platforms.get('codeforces'):
            director = CFDirector
        elif platform == Constant.available_platforms.get('leetcode'):
            director = LeetDirector  # type: ignore
        elif platform == Constant.available_platforms.get('codechef'):
            director = CodeChefDirector  # type: ignore
        elif platform == Constant.available_platforms.get('stackoverflow'):
            director = StackOverflowDirector  # type: ignore
        elif platform == Constant.available_platforms.get('twitter'):
            director = TwitterDirector  # type: ignore
        elif platform == Constant.available_platforms.get('medium'):
            director = MediumDirector  # type: ignore
        else:
            raise ValueError('unsupported platform: {0}'.format(platform))

        return director.construct(username, token, proxy)
