import pandas
import requests

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
        return response.text

    def get_odds(self, config=None):
        """
        Method to return a Dataframe object of scraped results.
        :param config: search criteria, type dict
        :return: Pandas Dataframe object
        """
        scr_data = pandas.read_html(self._get())[4]
        if config:
            if config['query'] is not None:
                data = scr_data
                return data
        else:
            return scr_data.to_html()

    def get_odds_telegram(self, config=None):
        """
        Method to return a Dataframe object of scraped results.
        :param config: search criteria, type dict
        :return: Pandas Dataframe object
        """
        scr_data = pandas.read_html(self._get())[4]
        if config:
            if config['query'] is not None:
                data = scr_data
                return data
        else:
            return scr_data

    def download(self, config=None):
        """
        Method to download .csv file of scraped results
        :param config: search criteria, type dict
        :return: Pandas Dataframe object
        """
        scr_data = pandas.read_html(self._get())[4]
        if config:
            if config['query'] is not None:
                data = scr_data
                return data
        else:
            return scr_data
