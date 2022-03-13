from collections import OrderedDict
from telegram.utils.types import JSONDict
from typing import Union
import time

def _find_next_id(ordered_dict: OrderedDict, last_id: int) -> int:
    next_id = last_id+1
    while next_id in ordered_dict:
        next_id+=1
    return next_id

def send_message(data: JSONDict, server) -> Union[JSONDict, bool]:
    last_message_id = list(server.messages[data["chat_id"]])[-1] if server.messages[data["chat_id"]] else 0
    new_message_id = _find_next_id(server.messages[data["chat_id"]], last_message_id)
    return {
        "message_id": new_message_id,
        "from": server.bot_user.to_dict(),
        "chat": {
            "id": data["chat_id"],
            "title": "...",
            "type": "group"
        },
        "date": time.time(),
        "text": data["text"]
    }
