from socialstats.base.director_interface import IDirector
from socialstats.medium.medium_builder import MediumBuilder


class MediumDirector(IDirector):
    """Director class for building medium user."""

    @staticmethod
    def construct(username: str, token: str = '', proxy: str = ''):
        """Construct codeforces user part by part."""
        return MediumBuilder(username) \
            .with_proxy(proxy) \
            .build_profile() \
            .return_user()
