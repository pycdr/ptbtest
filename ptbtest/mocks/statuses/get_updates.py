from time import sleep

from telegram import Update
from telegram.utils.types import JSONDict
from typing import Union

def get_updates(data: JSONDict, server) -> Union[JSONDict, bool]:
    sleep(.5)
    result = []
    while not server.new_updates.empty():
        update = server.new_updates.get()
        if isinstance(update, (Update)):
            update = update.to_dict()
        result.append(update)
    return result
