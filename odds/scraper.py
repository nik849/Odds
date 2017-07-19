import aiohttp
import asyncio

from .config import HOST_URL


class scrape:
    """
    Scraping class, using beautifulsoup4.
    """
    def __init__(self,
                 loop: Optional[asyncio.BaseEventLoop] = None,
                 session: aiohttp.ClientSession = None,):
        """
        """
        self.loop = loop or asyncio.get_event_loop()
        self.session = session or aiohttp.ClientSession(loop=self.loop)


    async def _get(self, session, port=None):
        """
        Method to scrape a single page and return a json object.
        :param session: Required for async
        :param port: Port for access Optional
        :return: json object containing scraped data
        """
        req_str = HOST_URL
        async with self.session.get(url=req_str) as response:
            assert response.status == 200
            data = await response.json()
        return data
