from datetime import datetime

from dateutil import relativedelta

from socialstats.base.user import BaseUser


class CFUser(BaseUser):
    """Codeforces user class."""

    org: str = ''
    rating: int = 0
    rank: int = 0
    max_rating: int = 0
    max_rank: str = ''
    contests: int = 0
    submissions: int = 0
    accepted: int = 0
    wrong_ans: int = 0
    tle: int = 0
    contributions: int = 0
    registration_unix_time: int = 0

    @property
    def rating_color(self):
        """Return the rating color."""
        return self._get_color(self.rating)

    @property
    def max_rating_color(self):
        """Return color of max_rating."""
        return self._get_color(self.max_rating)

    @property
    def member_since(self):
        """Return the number of years at codeforces."""
        joined_at = datetime.fromtimestamp(self.registration_unix_time)
        rd = relativedelta.relativedelta(datetime.now(), joined_at)
        return int(rd.years)

    @classmethod
    def _get_color(cls, rating):  # NOQA: WPS231
        """Return the HEX of appropriate color according to the rating."""
        if rating <= 1199:  # NOQA: WPS223
            col = '#cec8c1'
        elif 1199 < rating <= 1399:
            col = '#43A217'
        elif 1399 < rating <= 1599:
            col = '#22C4AE'
        elif 1599 < rating <= 1899:
            col = '#1427B2'
        elif 1899 < rating <= 2099:
            col = '#700CB0'
        elif 2099 < rating <= 2299:
            col = '#F9A908'
        elif 2299 < rating <= 2399:
            col = '#FBB948'
        else:
            col = '#FF0000'
        return col
