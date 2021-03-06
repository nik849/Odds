import requests

from .config import telegram_API_URL, totalcorner_API_URL
from .errors import OddsError, TelegramTokenError, TotalCornerTokenError


class telegram:
    """
    Wrapper Class for the Telegram API.
    Uses requests to get the returned json object.
    """
    def __init__(self, token):
        """
        :param token: Telegram API token, Required.
        """
        if not token:
            raise TelegramTokenError

        self.token = token
        self.params = {}

    def _get(self, api_endpoint, **kwargs):
        """
        Method for making a request to Telegram API
        :param api_endpoint: Telegram API endpoint
        """
        req_str = telegram_API_URL + 'bot' + self.token + '/' + api_endpoint
        response = requests.get(url=req_str, params=self.params)
        return response.json()

    def send_message(self, msg: str, chat_id: str, **kwargs):
        """
        :param msg: Message to be sent to users
        :param chat_id: Id of the user/channel to send message to.
        """
        if kwargs:
            self.params.update(**kwargs)

        self.params['chat_id'] = chat_id
        self.params['text'] = msg
        data = self._get('sendMessage', params=self.params)

        if not data['ok']:
            raise OddsError(str(data['description']))

        return data['result']

    def update(self):
        """
        Fetches new messages sent to the Bot.
        :return: array of json objects containing responses.
        """
        req_str = telegram_API_URL + 'bot' + self.token + '/getUpdates'
        response = requests.get(url=req_str)
        data = response.json()

        if not data['ok']:
            raise OddsError(str(data['description']))

        results = data['result']

        return [{'id': updates['update_id'],
                 'message': updates['message']
                 } for updates in results]

    def set_webhook(self, hook_url: str):
        """
        Sets the webhook for the telegram bot.
        :param hook_url: webhook url, found in config
        """
        req_str = telegram_API_URL + 'bot' + self.token + '/setWebhook'
        hook = hook_url + '/hook'
        params = {'url': hook}
        response = requests.get(url=req_str, params=params)
        assert response.status_code == 200

    def process_message(self, data: object):
        """
        Method for processing a request from a telegram user
        :param data: dict of user name and message
        :return: search criteria for the scraper
        """
        criteria = {'query': None}
        if data['message'] is not None:
            criteria['query'] = data['message']
            self.send_message('loading...', data['user'])
            print(criteria)
            return criteria
        return criteria


class totalcorner():
    """
    Wrapper class for totalcorner API_URL
    """
    def __init__(self, token):
        """
        :param token: TotalCorner API token, Required.
        """
        if not token:
            raise TotalCornerTokenError

        self.token = token
        self.params = {}

    def _get(self, api_endpoint, **kwargs):
        """
        Method for making a request to TotalCorner API
        :param api_endpoint: Totalcorner API endpoint
        """
        req_str = totalcorner_API_URL + api_endpoint
        response = requests.get(url=req_str, params=self.params)
        return response.json()

    def get_odds(self, **kwargs):
        """
        Method for retrieving odds from totalscore
        """
        if kwargs:
            self.params.update(**kwargs)
        self.params['token'] = self.token
        self.params['type'] = 'inplay'
        self.params['columns'] = "events,odds"

        data = self._get('match/today', params=self.params)

        if not data['success']:
            raise OddsError(str(data['error']))
            return 1
        return data["data"]

    def get_match_odds(self, match_id, **kwargs):
        """
        Method for retrieving odds for a specific match
        """
        self.match_id = match_id
        if kwargs:
            self.params.update(**kwargs)
        self.params['token'] = self.token
        self.params['columns'] = ['events', 'odds']

        req_str = f'matchodds/{self.match_id}'
        data = self._get(req_str, params=self.params)

        if not data['success']:
            raise OddsError(str(data['error']))
            return 1
        return data["data"]
