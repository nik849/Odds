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

    def get_odds_html(self, config=None):
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
            return scr_data.fillna(value='').to_html()

    def get_odds_obj(self, config=None):
        """
        Method to return a Dataframe object of scraped results.
        :param config: search criteria, type dict
        :return: Pandas Dataframe object
        """
        df = pandas.read_html(self._get())[4]
        indexes = df[df[0].str.contains(' - ', na=False)].index.tolist()
        df_dict = {}
        for i in list(range(len(indexes)-1)):
            current = indexes[i]
            nex = indexes[i + 1]
            df_dict[str(df.ix[indexes[i], 0])] = df[current:nex]

        if config:
            if config['query'] is not None:
                data = df_dict
                return data
        else:
            return df_dict

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
