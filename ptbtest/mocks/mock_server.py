from queue import Queue
from typing import IO, Dict, List, Tuple
from collections import OrderedDict
from ptbtest.generators.base import Generator
from telegram import Chat, PhotoSize, TelegramObject, Update, User, Message
from telegram.utils.types import JSONDict
from typing import Union
from .statuses import STATUSES

class MockServer:
    """
    This object is used in :class:`ptbtest.mocks.mocks_server.MockServer`
    to remove Telegram API part in test cases.
    """
    def __init__(self):
        self._bot_user: User = None
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
        # {chat_id -> {message_id: Message}}
        self._messages: Dict[int, OrderedDict] = {}
        # {file_id -> PhotoSize}
        self._files_id: Dict[str, PhotoSize] = {}
    
    @property
    def bot_user(self) -> User:
        """Bot's :class:`telegram.User` object"""
        return self._bot_user
    
    @property
    def users(self) -> Dict[int, User]:
        """Existing Users in mock telegram"""
        return self._users
    
    @property
    def chats(self) -> Dict[int, Chat]:
        """Existing Chats in mock telegram"""
        return self._chats
    
    @property
    def updates(self) -> OrderedDict:
        """All Updates in mock telegram"""
        return self._updates
    
    @property
    def bot_reactions(self) -> Queue:
        """Sent Message by the Mock Bot, catched by test cases"""
        return self._bot_reactions
    
    @property
    def new_updates(self) -> Queue:
        """Generated Updates in test cases, catched by bot"""
        return self._new_updates
    
    @property
    def messages(self) -> Dict[int, Dict[int, Message]]:
        """All Messages in mock telegram"""
        return self._messages

    @property
    def files_id(self) -> Dict[str, PhotoSize]:
        """All "file_id"s in mock telegram"""
        return self._files_id

    def insert_user(self, user: User):
        """Insert new :class:`telegram.User` into the mock telegram"""
        if not isinstance(user, User):
            raise TypeError(f"parameter \"user\" must be \"telegram.User\", not {type(user).__name__}")
        self.users[user.id] = user
        # Each User has also a Chat object itself..!
        if user.id not in self.chats:
            self.insert_chat(Chat(
                id=user.id, type=Chat.PRIVATE, username=user.username,
                first_name=user.first_name, last_name=user.last_name,
            ))

    def insert_chat(self, chat: Chat):
        """Insert new :class:`telegram.Chat` into the mock telegram"""
        if not isinstance(chat, Chat):
            raise TypeError(f"parameter \"chat\" must be \"telegram.Chat\", not {type(chat).__name__}")
        self.chats[chat.id] = chat
    
    def post(self, status: str, data: JSONDict) -> Union[JSONDict, bool]:
        """Send `data` to the mock telegram for `status` method"""
        if status not in STATUSES:
            raise ValueError(f"invalid status: {status}")
        return STATUSES[status](data, self)
    
    def set_bot_user(self, user: User) -> None:
        """Set the Bot's :class:`telegram.User` object"""
        self._bot_user = user
    
    def insert_update(self, update: Update) -> None:
        """Put new :class:`telegram.ext.Update` in `new_updates` queue"""
        self.new_updates.put(update)
    
    def send_to_bot(self, generator: Generator) -> None:
        """Config a new Generator and Insert into bot updates"""
        if not isinstance(generator, Generator):
            raise TypeError(f"parameter \"generator\" must be from type \"ptbtest.generators.base.Generator\", not {type(generator).__name__}")
        self.insert_update(generator.config(self))
