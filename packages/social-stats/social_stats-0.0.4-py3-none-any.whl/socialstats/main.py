from socialstats.factories.user_factory import UserFactory


def get_stat(platform: str, username: str, token: str = '', proxy: str = '') -> dict:
    """Return user information in dictionary format."""
    user = UserFactory.create_user(platform=platform, username=username, token=token, proxy=proxy)
    return dict(user)
