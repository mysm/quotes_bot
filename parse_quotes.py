import logging

import requests_cache
from bs4 import BeautifulSoup

from utils import get_response, find_tag, remove_punctuation

QUOTES_URL = "https://socratify.net/quotes/random"

logger = logging.getLogger(__name__)


def get_random_quote(clear_cache=False):

    session = requests_cache.CachedSession()
    if clear_cache:
        session.cache.clear()

    response = get_response(session, QUOTES_URL)

    soup = BeautifulSoup(response.text, features="lxml")

    result = {"quotes": "", "author": "", "source": ""}

    tag = find_tag(soup, "h1", {"class": "b-quote__text"})
    if tag:
        result["quotes"] = tag.text

    tag = find_tag(soup, "h2", {"class": "b-quote__category"})
    if tag:
        href = find_tag(tag, "a")
        if href:
            result["source"] = href["href"]
            result["author"] = remove_punctuation(href.text.split('\n')[1].lstrip())

    return result


if __name__ == "__main__":
    print(get_random_quote())
