import re

import requests
from bs4 import BeautifulSoup

from socialstats.base.proxy_mixin import ProxyMixin
from socialstats.codechef.cc_user import CodeChefUser
from socialstats.constant import Constant


class CodeChefBuilder(ProxyMixin):
    """Codechef stat builder class."""

    user = CodeChefUser()

    def __init__(self, username: str):
        """Construct builder."""
        self.user.username = username

    def _scrap_data(self):
        """Scrap codechef profile data."""
        scrapped_data = {}
        try:
            response = requests.get(
                Constant.codechef_web_endpoint.format(self.user.username),
                proxies=self._proxies,
            )
        except Exception:
            raise ValueError('Could not load the codechef website.')
        soup = BeautifulSoup(response.text, 'lxml')

        scrapped_data['name'] = soup.find('h1', class_='h2-style').text
        scrapped_data['avatar_url'] = soup.find('img', class_='profileImage').get('src')

        star_text = soup.find('span', class_='rating').text
        scrapped_data['star'] = re.findall(r'\d+', star_text)[0]

        scrapped_data['country'] = soup.find('span', class_='user-country-name').text

        star_text = soup.find('a', class_='rating').text
        scrapped_data['rating'] = re.findall(r'\d+', star_text)[0]

        lis = soup.find_all('li')
        for li in lis:
            if 'Motto' in li.text:
                scrapped_data['motto'] = li.text.replace('Motto:', '')
            elif 'Student/Professional' in li.text:
                scrapped_data['profession'] = li.text.replace('Student/Professional:', '')
            elif 'Institution' in li.text:
                scrapped_data['org'] = li.text.replace('Institution:', '')

        solved_html = soup.find('section', class_='rating-data-section problems-solved').h5.text
        scrapped_data['solved'] = re.findall(r'\d+', solved_html)[0]

        contribution_html = soup.find_all('h5', class_='collapse')
        for h5 in contribution_html:
            if 'Authored' in h5.text:
                scrapped_data['authored'] = re.findall(r'\d+', h5.text)[0]
            elif 'Tested' in h5.text:
                scrapped_data['tested'] = re.findall(r'\d+', h5.text)[0]
            elif 'Contributed' in h5.text:
                scrapped_data['contributed'] = re.findall(r'\d+', h5.text)[0]

        small_tags = soup.find_all('small')
        for tag in small_tags:
            if 'Highest Rating' in tag.text:
                scrapped_data['highest_rating'] = re.findall(r'\d+', tag.text)[0]

        return scrapped_data

    def build_profile(self):
        """Build user basic profile info."""
        scrapped_data = self._scrap_data()
        self.user.first_name = scrapped_data.get('name')
        self.user.avatar_url = scrapped_data.get('avatar_url')
        self.user.star = scrapped_data.get('star')
        self.user.rating = scrapped_data.get('rating')
        self.user.highest_rating = scrapped_data.get('highest_rating')
        self.user.motto = scrapped_data.get('motto')
        self.user.profession = scrapped_data.get('profession')
        self.user.country = scrapped_data.get('country')
        self.user.org = scrapped_data.get('org')
        self.user.solved = scrapped_data.get('solved')
        self.user.authored = scrapped_data.get('authored')
        self.user.tested = scrapped_data.get('tested')
        self.user.contributed = scrapped_data.get('contributed')

        return self

    def return_user(self):
        """Return an instance of user."""
        return self.user
