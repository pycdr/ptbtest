import logging
from queue import Queue
from telegram import Bot, ReplyMarkup, Message, User, BotCommand
from telegram.utils.request import Request
from telegram.utils.types import JSONDict, ODVInput
from typing import Union, Optional, List

class MockBot(Bot):
    def __init__(self, token: str, request: 'Request' = None):
        self.token = self._validate_token(token)
        self.defaults = None
        base_url = 'https://api.telegram.org/bot'
        base_file_url = 'https://api.telegram.org/file/bot'
        self.base_url = str(base_url) + str(self.token)
        self.base_file_url = str(base_file_url) + str(self.token)
        self._bot: Optional[User] = None
        self._commands: Optional[List[BotCommand]] = None
        self._request = request or Request()
        self.private_key = None
        self.logger = logging.getLogger(__name__)
        self.bot_messages = Queue()
    
    def _message(
        self, endpoint: str, data: JSONDict, 
        reply_to_message_id: int = None, 
        disable_notification: ODVInput[bool] = ..., 
        reply_markup: ReplyMarkup = None, 
        allow_sending_without_reply: ODVInput[bool] = ..., 
        timeout: ODVInput[float] = ..., 
        api_kwargs: JSONDict = None
    ) -> Union[bool, Message]:
        result_message = super()._message(
            endpoint, data, reply_to_message_id, 
            disable_notification, reply_markup, 
            allow_sending_without_reply, timeout, api_kwargs
        )
        self.bot_messages.put(result_message)
        return result_message

