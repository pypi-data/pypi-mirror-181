from types import MappingProxyType


class Constant:
    """Class for organizing constants."""

    # API endpoints

    # codeforces endpoints
    cf_user_info = 'https://codeforces.com/api/user.info?handles={0}'
    cf_user_status = 'https://codeforces.com/api/user.status?handle={0}'
    cf_user_rating = 'https://codeforces.com/api/user.rating?handle={0}'

    # leet-code endpoints
    leetcode_api_endpoint = 'https://leetcode.com/graphql'

    # codechef endpoint
    codechef_web_endpoint = 'https://www.codechef.com/users/{0}'

    # stackoverflow endpoint
    stack_overflow_endpoint = 'https://api.stackexchange.com/2.3/users/{0}?site=stackoverflow'

    # twitter endpoint
    twitter_endpoint = 'https://api.twitter.com/2/users/by/username/{0}?user.fields=public_metrics'

    # medium endpoint
    medium_endpoint = 'https://medium.com/{0}?format=json'
    json_hijacking_prefix = '])}while(1);</x>'

    available_platforms = MappingProxyType({
        'codeforces': 'codeforces',
        'leetcode': 'leetcode',
        'codechef': 'codechef',
        'stackoverflow': 'stackoverflow',
        'twitter': 'twitter',
        'medium': 'medium',
    })
