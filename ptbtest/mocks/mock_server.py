from queue import Queue
from typing import Dict, List
from collections import OrderedDict
from ptbtest.generators.base import Generator
from telegram import Chat, TelegramObject, Update, User, Message
from telegram.utils.types import JSONDict
from typing import Union
from .statuses import STATUSES

class MockServer:
    def __init__(self):
        # {user_id -> User}
        self._users: Dict[int, User] = {}
        # {chat_id -> Chat}
        self._chats: Dict[int, Chat] = {}
        # {update_id -> Update}
        self._updates: OrderedDict = OrderedDict({})
        # Queue: Message | ...
        self._bot_reactions: Queue = Queue()
        # Queue: Update
        self._new_updates: Queue = Queue()
        self._bot_user: User = None
        # {chat_id -> {message_id: Message}}
        self._messages: Dict[int, OrderedDict] = {}
    
    @property
    def bot_user(self) -> User:
        return self._bot_user
    
    @property
    def users(self) -> Dict[int, User]:
        return self._users
    
    @property
    def chats(self) -> Dict[int, Chat]:
        return self._chats
    
    @property
    def updates(self) -> OrderedDict:
        return self._updates
    
    @property
    def bot_reactions(self) -> Queue:
        return self._bot_reactions
    
    @property
    def new_updates(self) -> Queue:
        return self._new_updates
    
    @property
    def messages(self) -> Dict[int, Dict[int, Message]]:
        return self._messages

    def insert_user(self, user: User):
        if not isinstance(user, User):
            raise TypeError(f"parameter \"user\" must be \"telegram.User\", not {type(user).__name__}")
        self.users[user.id] = user
        if user.id not in self.chats:
            self.insert_chat(Chat(
                id=user.id, type=Chat.PRIVATE, username=user.username,
                first_name=user.first_name, last_name=user.last_name,
            ))

    def insert_chat(self, chat: Chat):
        if not isinstance(chat, Chat):
            raise TypeError(f"parameter \"chat\" must be \"telegram.Chat\", not {type(chat).__name__}")
        self.chats[chat.id] = chat
    
    def post(self, status: str, data: JSONDict) -> Union[JSONDict, bool]:
        if status not in STATUSES:
            raise ValueError(f"invalid status: {status}")
        return STATUSES[status](data, self)
    
    def set_bot_user(self, user: User) -> None:
        self._bot_user = user
    
    def insert_update(self, update: Update) -> None:
        self.new_updates.put(update)
    
    def send_to_bot(self, generator: Generator) -> None:
        if not isinstance(generator, Generator):
            raise TypeError(f"parameter \"generator\" mus be from type \"ptbtest.generators.base.Generator\", not {type(generator).__name__}")
        self.insert_update(generator.config(self))
