import requests
from marshmallow import ValidationError

from todolist.bot.tg.dc import GetUpdatesResponse, GetUpdatesResponseSchema, SendMessageResponse, \
    SendMessageResponseSchema


class TgClient:
    def __init__(self, token):
        self.__token = token

    @property
    def token(self):
        return self.__token

    def get_url(self, method: str) -> str:

        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        url: str = self.get_url(method='getUpdates')
        params: dict[str, int] = {'offset': offset, 'timeout': timeout}
        response = requests.get(url, params=params).json()
        return GetUpdatesResponseSchema().load(response)

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        url: str = self.get_url(method='sendMessage')
        data: dict[str, int | str] = {
            'chat_id': chat_id,
            'text': text
        }
        response = requests.post(url, json=data).json()
        try:
            return SendMessageResponseSchema().load(response)
        except ValidationError:
            return response
