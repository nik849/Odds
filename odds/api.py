import requests

from .config import API_URL, test_token, chat_id
from .errors import OddsError, TelegramTokenError


class telegram:
    """
    Wrapper Class for the Telegram API.
    Uses requests to get the returned json object.
    """
    def __init__(self, token=test_token):
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
        req_str = API_URL + 'bot' + self.token + '/' + api_endpoint
        print(req_str)
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
