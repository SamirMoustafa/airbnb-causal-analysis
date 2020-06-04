import itertools
import os

import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

import urllib.request

from tqdm import tqdm

from src.utils import save_to_file

AIRBNB_LINK = "http://insideairbnb.com/get-the-data.html"
AIRBNB_DATASET_FILENAME = 'airbnb_dataset_links.csv'
csv_file_name = 's/listings.csv'
LINK = 'link'
INDEX2KEY = {3: 'country',
             4: 'location',
             5: 'city',
             6: 'date', }


def __scrape__():
    # TODO: add warring that this process will take time
    html_page = urlopen(AIRBNB_LINK)
    soup = BeautifulSoup(html_page, "html.parser")
    return [link.get('href') for link in soup.findAll('a', attrs={'href': re.compile("^http://")})]


class AirbnbLinksScraper(object):
    def __init__(self, scrape=False):
        if scrape:
            self.links = __scrape__()

    def __pre_processing__(self, links=None):

        if (not links) and (not hasattr(self, 'links')):
            raise ValueError('no links to do pre-processing on it, use scrape function, or pass `True` to the '
                             'constructor')

        if not links:
            links = self.links

        has_word = lambda text, word: text if word in text else None

        filtered_links = list(map(has_word, links, itertools.repeat(csv_file_name, len(links))))
        filtered_links = list(filter(None.__ne__, filtered_links))
        return filtered_links

    def __call__(self, file_path):

        if os.path.exists(file_path):
            if pd.read_csv(file_path).shape[0] >= 2565:
                return True

        links = __scrape__()
        filtered_links = self.__pre_processing__(links)

        for link in filtered_links:
            dict_saver = {}
            for key in INDEX2KEY.keys():
                split_link = link.split('/')
                dict_saver.update({INDEX2KEY[key]: split_link[key]})

            dict_saver.update({LINK: link})
            save_to_file(file_path, dict_saver)
        return True


def find_airbnb_link(country, location, city, date):
    df = pd.read_csv(AIRBNB_DATASET_FILENAME)
    df_target = df.loc[df['country'] == country]
    df_target = df_target.loc[df_target['location'] == location]
    df_target = df_target.loc[df_target['city'] == city]
    df_target = df_target.loc[df_target['date'] == date]

    if df_target.shape[0] == 0:
        raise ValueError('can\'t find the target values in our dataset')

    return df_target[LINK].iloc[0]


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, t_size=None):
        if t_size is not None:
            self.total = t_size
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)


if __name__ == '__main__':
    # simple test for the scraper
    target_info = {'country': 'canada',
                   'location': 'on',
                   'city': 'toronto',
                   'date': '2020-05-07', }
    output_file_name = 'toronto_2020-05-07.csv'

    # start testing
    scraper = AirbnbLinksScraper()
    scraper(AIRBNB_DATASET_FILENAME)
    link = find_airbnb_link(target_info['country'], target_info['location'],
                            target_info['city'],    target_info['date'])

    download_url(link, output_file_name)
