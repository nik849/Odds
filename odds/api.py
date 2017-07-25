import requests

from .config import API_URL, WEBHOOK_URL
from .errors import OddsError, TelegramTokenError


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
        req_str = API_URL + 'bot' + self.token + '/' + api_endpoint
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
        req_str = API_URL + 'bot' + self.token + '/getUpdates'
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
        req_str = API_URL + 'bot' + self.token + '/setWebhook'
        params = {'url': hook_url}
        response = requests.get(url=req_str, params=params)
        assert response.status_code == 200
