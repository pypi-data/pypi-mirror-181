from socialstats.base.director_interface import IDirector
from socialstats.leetcode.leet_builder import LeetBuilder


class LeetDirector(IDirector):
    """Director class for building leetcode user."""

    @staticmethod
    def construct(username: str, token: str = '', proxy: str = ''):
        """Construct leetcode user part by part."""
        return LeetBuilder(username) \
            .with_proxy(proxy) \
            .build_basic_profile() \
            .build_submission_info() \
            .build_contest_info() \
            .return_user()
