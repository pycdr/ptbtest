from collections import OrderedDict
import os, random, string, time, io
from PIL import Image

from telegram import PhotoSize
from telegram.utils.types import JSONDict
from typing import Dict, Union

def _find_next_int_id(ordered_dict: OrderedDict, last_id: int) -> int:
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

def send_message(data: JSONDict, server) -> Union[JSONDict, bool]:
    last_message_id = list(server.messages[data["chat_id"]])[-1] if server.messages[data["chat_id"]] else 0
    new_message_id = _find_next_int_id(server.messages[data["chat_id"]], last_message_id)
    return {
        "message_id": new_message_id,
        "from": server.bot_user.to_dict(),
        "chat": server.chats[data["chat_id"]].to_dict(),
        "date": time.time(),
        "text": data["text"]
    }

def send_photo(data: JSONDict, server) -> JSONDict:
    last_message_id = list(server.messages[data["chat_id"]])[-1] if server.messages[data["chat_id"]] else 0
    new_message_id = _find_next_int_id(server.messages[data["chat_id"]], last_message_id)
    if data["photo"] not in server.files_id:
        new_file_id = _find_next_str_id(server.files_id, 88)
        new_file_unique_id = _find_next_str_id([], 16)
        width, height = Image.open(data["photo"]).size
        res_photo = PhotoSize(
            file_id=new_file_id,
            file_unique_id=new_file_unique_id,
            width=width,
            height=height,
            file_size=os.stat(data["photo"].name if isinstance(data["photo"], io.BufferedReader) else data["photo"]).st_size,
        )
        server.files_id[new_file_id] = res_photo
    else:
        res_photo = server.files_id[data["photo"]]
    return {
        "message_id": new_message_id,
        "from": server.bot_user.to_dict(),
        "chat": server.chats[data["chat_id"]].to_dict(),
        "date": time.time(),
        "photo": [res_photo.to_dict()],
        "caption": data.get("caption", None),
    }
