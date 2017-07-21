import requests
from bs4 import BeautifulSoup

from .config import HOST_URL


class scrape:
    """
    Scraping class, using asyncio and aiophttp.
    """
    def __init__(self):
        """
        Initialiser for scrape class.
        """

    def _get(self, port=None):
        """
        Method to scrape a single page and return a json object.
        :param port: Port for access Optional
        :return: text object containing scraped data
        """
        req_str = HOST_URL
        response = requests.get(url=req_str)
        assert response.status_code == 200
        soup = BeautifulSoup(response.content)

        tbl = soup.findAll('table')[4]
        return tbl
