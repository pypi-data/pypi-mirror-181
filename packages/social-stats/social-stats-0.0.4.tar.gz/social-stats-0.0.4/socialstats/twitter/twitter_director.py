from socialstats.base.director_interface import IDirector
from socialstats.twitter.twitter_builder import TwitterBuilder


class TwitterDirector(IDirector):
    """Director class for building Twitter user."""

    @staticmethod
    def construct(username: str, token: str = '', proxy: str = ''):
        """Construct codechef user part by part."""
        if not token:
            raise ValueError('Token is required for Twitter API.')
        return TwitterBuilder(username, token=token) \
            .with_proxy(proxy) \
            .build_profile() \
            .return_user()
