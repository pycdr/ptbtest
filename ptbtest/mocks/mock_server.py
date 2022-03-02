from typing import Dict, List, Callable
from telegram import Chat, TelegramObject, User
from telegram.utils.types import JSONDict
from typing import Union
import pdb

STATUSES: Dict[str, Callable[[JSONDict], Union[JSONDict, bool]]] = {
}

class MockServer:
    def __init__(self):
        self._users: Dict[int, User] = {}
        self._chats: Dict[int, Chat] = {}
        self._bot_reactions: List[TelegramObject] = []
    
    @property
    def users(self) -> Dict[int, User]:
        return self._users
    
    @property
    def chats(self) -> Dict[int, Chat]:
        return self._chats
    
    @property
    def bot_reactions(self) -> List[TelegramObject]:
        return self._bot_reactions

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
        return STATUSES[status](data)
