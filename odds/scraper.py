import asyncio
from typing import Optional

import aiohttp

from .config import HOST_URL


class scrape:
    """
    Scraping class, using asyncio and aiophttp.
    """
    def __init__(self,
                 loop: Optional[asyncio.BaseEventLoop] = None,
                 session: aiohttp.ClientSession = None):
        """
        Initialiser for scrape class.
        """
        self.loop = loop or asyncio.get_event_loop()
        self.session = session or aiohttp.ClientSession(loop=self.loop)

    async def _get(self, port=None):
        """
        Method to scrape a single page and return a json object.
        :param port: Port for access Optional
        :return: text object containing scraped data
        """
        req_str = HOST_URL
        async with self.session.get(url=req_str) as response:
            assert response.status == 200
            data = await response.text()
        return data
