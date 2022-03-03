from queue import Queue
from typing import Dict, List
from telegram import Chat, TelegramObject, Update, User
from telegram.utils.types import JSONDict
from typing import Union
from .statuses import STATUSES

class MockServer:
    def __init__(self):
        self._users: Dict[int, User] = {}
        self._chats: Dict[int, Chat] = {}
        self._bot_reactions: Queue = Queue()
        self._updates: Queue = Queue()
        self._bot_user: User = None
    
    @property
    def users(self) -> Dict[int, User]:
        return self._users
    
    @property
    def chats(self) -> Dict[int, Chat]:
        return self._chats
    
    @property
    def bot_reactions(self) -> List[TelegramObject]:
        return self._bot_reactions
    
    @property
    def updates(self) -> List[TelegramObject]:
        return self._updates

    def insert_user(self, user: User):
        if not isinstance(user, User):
            raise TypeError(f"parameter \"user\" must be \"telegram.User\", not {type(user).__name__}")
        self.users[user.id] = user

    def insert_chat(self, chat: Chat):
        if not isinstance(chat, User):
            raise TypeError(f"parameter \"chat\" must be \"telegram.Chat\", not {type(chat).__name__}")
        self.users[chat.id] = chat
    
    def post(self, status: str, data: JSONDict) -> Union[JSONDict, bool]:
        if status not in STATUSES:
            raise ValueError(f"invalid status: {status}")
        return STATUSES[status](data, self)
    
    def set_bot_user(self, user: User) -> None:
        self._bot_user = user
