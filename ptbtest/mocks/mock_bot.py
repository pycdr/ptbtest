import logging
from telegram import Bot, ReplyMarkup, Message, User, BotCommand
from telegram.utils.request import Request
from telegram.utils.types import JSONDict, ODVInput
from typing import Union, Optional, List
from .mock_request import MockRequest

class MockBot(Bot):
    def __init__(self, token: str, bot_user: User, request: 'MockRequest' = None):
        self.token = self._validate_token(token)
        self.defaults = None
        base_url = 'https://api.telegram.org/bot'
        base_file_url = 'https://api.telegram.org/file/bot'
        self.base_url = str(base_url) + str(self.token)
        self.base_file_url = str(base_file_url) + str(self.token)
        self._commands: Optional[List[BotCommand]] = None
        self._bot = bot_user or User(
            id=0, first_name="MockBot", is_bot=True,
            username="mockbot", can_join_groups=False,
            can_read_all_group_messages=True,
            supports_inline_queries=True
        )
        self.private_key = None
        self.logger = logging.getLogger(__name__)
        self._request: MockRequest = request or MockRequest()
        self._request.server.set_bot_user(self._bot)
    
    def _message(
        self, endpoint: str, data: JSONDict, 
        reply_to_message_id: int = None, 
        disable_notification: ODVInput[bool] = ..., 
        reply_markup: ReplyMarkup = None, 
        allow_sending_without_reply: ODVInput[bool] = ..., 
        timeout: ODVInput[float] = ..., 
        api_kwargs: JSONDict = None, 
        protect_content=None
    ) -> Union[bool, Message]:
        result_message: Message = super()._message(
            endpoint, data, reply_to_message_id, 
            disable_notification, reply_markup, 
            allow_sending_without_reply, timeout, 
            api_kwargs, protect_content
        )
        self.request.server.messages[result_message.chat.id][result_message.message_id] = result_message
        self.request.server.bot_reactions.put(result_message)
        return result_message
