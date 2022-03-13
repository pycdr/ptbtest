from collections import OrderedDict
from datetime import datetime
from typing import Union, Tuple, List
from .base import Generator
from telegram import Chat, Message, ReplyMarkup, MessageEntity, Update, User
from telegram.utils.types import ODVInput, DVInput, JSONDict
from telegram.utils.helpers import DEFAULT_NONE

def _find_next_id(ordered_dict: OrderedDict, last_id: int) -> int:
    next_id = last_id+1
    while next_id in ordered_dict:
        next_id+=1
    return next_id

class SendMessageGenerator(Generator):
    def __init__(
        self, 
        chat_id: Union[int, str], 
        user_id: Union[int, str], 
        text: str, 
        parse_mode: ODVInput[str] = DEFAULT_NONE,
        disable_web_page_preview: ODVInput[bool] = DEFAULT_NONE,
        disable_notification: DVInput[bool] = DEFAULT_NONE,
        reply_to_message_id: int = None,
        reply_markup: ReplyMarkup = None,
        timeout: ODVInput[float] = DEFAULT_NONE,
        api_kwargs: JSONDict = None,
        allow_sending_without_reply: ODVInput[bool] = DEFAULT_NONE,
        entities: Union[List['MessageEntity'], Tuple['MessageEntity', ...]] = None,
        protect_content: bool = None,
    ):
        self.chat_id = int(chat_id)
        self.user_id = int(user_id)
        self.text = text
        self.parse_mode = parse_mode
        self.disable_web_page_preview = disable_web_page_preview
        self.disable_notification = disable_notification
        self.reply_to_message_id = reply_to_message_id
        self.reply_markup = reply_markup
        self.timeout = timeout
        self.api_kwargs = api_kwargs
        self.allow_sending_without_reply = allow_sending_without_reply
        self.entities = entities
        self.protect_content = protect_content
    
    def config(self, server):
        last_update_id = list(server.updates)[-1] if server.updates else 0
        new_update_id = _find_next_id(server.updates, last_update_id)
        last_message_id = list(server.messages)[-1] if server.messages else 0
        new_message_id = _find_next_id(server.messages, last_message_id)
        self.update_id = new_update_id
        self.message_id = new_message_id
        self.chat = server.chats[self.chat_id]
        self.user = server.users[self.user_id]
        self.result_message = Message(
            message_id=self.message_id,
            date=datetime.now(),
            chat=self.chat,
            from_user=self.user,
            text=self.text,
            parse_mode=self.parse_mode,
            disable_web_page_preview = self.disable_web_page_preview,
            disable_notification = self.disable_notification,
            reply_to_message_id = self.reply_to_message_id,
            reply_markup = self.reply_markup,
            timeout = self.timeout,
            api_kwargs = self.api_kwargs,
            allow_sending_without_reply = self.allow_sending_without_reply,
            entities = self.entities,
            protect_content = self.protect_content,
        )
        if self.chat_id not in server.messages:
            server.messages[self.chat_id] = OrderedDict()
        server.messages[self.chat_id][new_message_id] = self.result_message
        server.updates[new_update_id] = self.to_update()
        return server.updates[new_update_id]
    
    def to_update(self) -> Update:
        return Update(
            update_id=self.update_id,
            message=self.result_message,
        )
