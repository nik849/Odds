class TelegramTokenError(Exception):
    msg = 'Missing Telegram token, ' \
          'visit:https://core.telegram.org/ ' \
          'to obtain a token'

    def __str__(self):
        return self.msg


class OddsBaseError(Exception):
    def __init__(self, msg):
        self.msg = msg


class OddsError(OddsBaseError):
    def __init__(self, msg):
        super().__init__(msg)

    def __str__(self):
        return self.msg
