from telegram.utils.types import JSONDict
from typing import Union

def get_me(data: JSONDict, server) -> Union[JSONDict, bool]:
    return server.bot_user.to_dict()
