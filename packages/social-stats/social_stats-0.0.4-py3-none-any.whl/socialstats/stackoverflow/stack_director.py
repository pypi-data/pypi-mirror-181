from socialstats.base.director_interface import IDirector
from socialstats.stackoverflow.stack_builder import StackOverflowBuilder


class StackOverflowDirector(IDirector):
    """Director class for building stackoverflow user."""

    @staticmethod
    def construct(username: str, token: str = '', proxy: str = ''):
        """Construct codechef user part by part."""
        if not token:
            raise ValueError('Token is required for stackoverflow API.')
        return StackOverflowBuilder(username, key=token) \
            .with_proxy(proxy) \
            .build_profile() \
            .return_user()
