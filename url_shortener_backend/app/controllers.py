import string
import random

LENGTH_SHORT_URL = 6
url_mapping = {}

def find_url(url_to_check):
    for short_url, url_info in url_mapping.items():
        if url_info['url'] == url_to_check:
            return short_url
    return None

def generate_short_url():
    while True:
        short_url = ''.join(random.choices(string.ascii_uppercase + string.digits, k=LENGTH_SHORT_URL))
        if short_url not in url_mapping:
            return short_url
        

def add_url(short_url, url):
    url_mapping[short_url] = {'url': url, 'visits': 0}


def get_url(short_url):
    if short_url in url_mapping:
        return url_mapping[short_url]['url']
    else:
        return None

def increment_visitis_counter(short_url):
    url_mapping[short_url]['visits'] += 1


def get_visits_counter(short_url):
    if short_url in url_mapping:
        return url_mapping[short_url]['visits']
    else:
        return None

