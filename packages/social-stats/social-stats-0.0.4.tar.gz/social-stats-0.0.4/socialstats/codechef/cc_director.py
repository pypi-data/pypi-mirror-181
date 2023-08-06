from socialstats.base.director_interface import IDirector
from socialstats.codechef.cc_builder import CodeChefBuilder


class CodeChefDirector(IDirector):
    """Director class for building codechef user."""

    @staticmethod
    def construct(username: str, token: str = '', proxy: str = ''):
        """Construct codechef user part by part."""
        return CodeChefBuilder(username) \
            .with_proxy(proxy) \
            .build_profile() \
            .return_user()
