"""This module contains the mock class of :class:`telegram.Bot`"""

import logging
from telegram import Bot, ReplyMarkup, Message, User, BotCommand
from telegram.utils.request import Request
from telegram.utils.types import JSONDict, ODVInput
from typing import Union, Optional, List
from .mock_request import MockRequest

class MockBot(Bot):
    """
    This object represents a mock object for :class:`telegram.Bot`.
    Args:
        token (:obj:`str`): Bot's token.
        bot_user (:obj:`telegram.User`): Bot's :obj:`User` attribute.
        request (:obj:`ptbtest.mocks.mock_request.MockRequest`, optional): request object. 
            default is :obj:`None`.
    """
    def __init__(self, token: str, bot_user: User, request: 'MockRequest' = None):
        # we still don't need to change or check any special thing here.
        self.token = self._validate_token(token)
        self.defaults = None
        base_url = 'https://api.telegram.org/bot'
        base_file_url = 'https://api.telegram.org/file/bot'
        self.base_url = str(base_url) + str(self.token)
        self.base_file_url = str(base_file_url) + str(self.token)
        self._commands: Optional[List[BotCommand]] = None
        self.private_key = None
        self.logger = logging.getLogger(__name__)
        # but, here... if bot_user==None, then use the default telegram.User object.
        self._bot = bot_user or User(
            id=0, first_name="MockBot", is_bot=True,
            username="mockbot", can_join_groups=False,
            can_read_all_group_messages=True,
            supports_inline_queries=True
        )
        # use `request` or create a mock request which ignores using Telegram API.
        self._request: MockRequest = request or MockRequest()
        # save bot user in MockServer object.
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
        # we need to catch the message which is sent by the bot.
        # it uses mock request automatically.
        # i.g. when you use `bot.send_message` method, it'll use
        # `bot._message` (see its source code), and we'll get
        # the generated `Message` object of sent message.
        result_message: Message = super()._message(
            endpoint, data, reply_to_message_id, 
            disable_notification, reply_markup, 
            allow_sending_without_reply, timeout, 
            api_kwargs, protect_content
        )
        # save the message in mock server data for the chat.
        self.request.server.messages[result_message.chat.id][result_message.message_id] = result_message
        # save the message in `bot_reactions`. so you'll be able
        # to get it in your test case and check it.
        self.request.server.bot_reactions.put(result_message)
        # return the message, so it won't effect your main bot.
        return result_message
