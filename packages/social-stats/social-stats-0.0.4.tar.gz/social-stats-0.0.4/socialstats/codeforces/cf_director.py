from socialstats.base.director_interface import IDirector
from socialstats.codeforces.cf_builder import CFBuilder


class CFDirector(IDirector):
    """Director class for building codeforces user."""

    @staticmethod
    def construct(username: str, token: str = '', proxy: str = ''):
        """Construct codeforces user part by part."""
        return CFBuilder(username) \
            .with_proxy(proxy) \
            .build_user_info() \
            .build_user_submission() \
            .build_rating_changes() \
            .return_user()
