from collections import OrderedDict
from datetime import datetime
import io, os, random, string
from PIL import Image
from typing import Dict, Union, Tuple, List
from .base import Generator
from telegram import Chat, Message, PhotoSize, ReplyMarkup, MessageEntity, Update, User
from telegram.utils.types import ODVInput, DVInput, JSONDict, FileInput
from telegram.utils.helpers import DEFAULT_NONE, DEFAULT_20

def _find_next_int_id(ordered_dict: OrderedDict, last_id: int) -> int:
    """returns the last id + 1 :/"""
    next_id = last_id+1
    while next_id in ordered_dict:
        next_id+=1
    return next_id

def _find_next_str_id(dict_: Dict, length: int) -> int:
    next_id = "".join(
        random.choice(string.ascii_letters+string.digits+"_-")
        for _ in range(length)
    )
    while next_id in dict_:
        # sorry, but I just wanna be completely sure..!
        next_id = "".join(
            random.choice(string.ascii_letters+string.digits+"_-")
            for _ in range(length)
        )
    return next_id

class SendMessageGenerator(Generator):
    """Message Update Generator Class"""
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
        new_update_id = _find_next_int_id(server.updates, last_update_id)
        last_message_id = list(server.messages)[-1] if server.messages else 0
        new_message_id = _find_next_int_id(server.messages, last_message_id)
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

class SendPhotoGenerator(Generator):
    """Photo Update Generator Class"""
    def __init__(
        self, 
        chat_id: Union[int, str], 
        user_id: Union[int, str], 
        photo: Union[FileInput, 'PhotoSize'], 
        caption: str = None, 
        disable_notification: DVInput[bool] = DEFAULT_NONE, 
        reply_to_message_id: int = None, 
        reply_markup: ReplyMarkup = None, 
        timeout: DVInput[float] = DEFAULT_20, 
        parse_mode: ODVInput[str] = DEFAULT_NONE, 
        api_kwargs: JSONDict = None, 
        allow_sending_without_reply: ODVInput[bool] = DEFAULT_NONE, 
        caption_entities: Union[List['MessageEntity'], Tuple['MessageEntity', ...]] = None, 
        filename: str = None, 
    ):
        self.chat_id = int(chat_id)
        self.user_id = int(user_id)
        self.photo = photo
        self.caption = caption
        self.parse_mode = parse_mode
        self.disable_notification = disable_notification
        self.reply_to_message_id = reply_to_message_id
        self.reply_markup = reply_markup
        self.timeout = timeout
        self.api_kwargs = api_kwargs
        self.allow_sending_without_reply = allow_sending_without_reply
        self.caption_entities = caption_entities
        self.filename = filename
    
    def config(self, server):
        last_update_id = list(server.updates)[-1] if server.updates else 0
        new_update_id = _find_next_int_id(server.updates, last_update_id)
        last_message_id = list(server.messages)[-1] if server.messages else 0
        new_message_id = _find_next_int_id(server.messages, last_message_id)
        self.update_id = new_update_id
        self.message_id = new_message_id
        self.chat = server.chats[self.chat_id]
        self.user = server.users[self.user_id]
        new_file_id = _find_next_str_id(server.files_id, 88)
        new_file_unique_id = _find_next_str_id([], 16)
        width, height = Image.open(self.photo).size
        res_photo = PhotoSize(
            file_id=new_file_id,
            file_unique_id=new_file_unique_id,
            width=width,
            height=height,
            file_size=os.stat(self.photo.name if isinstance(self.photo, io.BufferedReader) else self.photo).st_size,
        )
        server.files_id[new_file_id] = res_photo
        self.result_message = Message(
            message_id=self.message_id,
            date=datetime.now(),
            chat=self.chat,
            from_user=self.user,
            caption=self.caption,
            photo=[res_photo],
            parse_mode=self.parse_mode,
            disable_notification = self.disable_notification,
            reply_to_message_id = self.reply_to_message_id,
            reply_markup = self.reply_markup,
            timeout = self.timeout,
            api_kwargs = self.api_kwargs,
            allow_sending_without_reply = self.allow_sending_without_reply,
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
