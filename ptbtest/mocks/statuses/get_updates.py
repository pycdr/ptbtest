from time import sleep
from telegram.utils.types import JSONDict
from typing import Union

def get_updates(data: JSONDict, server) -> Union[JSONDict, bool]:
    sleep(.5)
    result = []
    while not server.updates.empty():
        result.append(server.updates.get())
    return result
