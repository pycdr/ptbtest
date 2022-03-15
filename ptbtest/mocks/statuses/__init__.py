"""This module used in MockRequest and MockServer to be used instead of main telegram API."""

from typing import Any, Dict, List, Callable, Union
from telegram.utils.types import JSONDict

from .get_me import get_me
from .webhook import delete_webhook
from .get_updates import get_updates
from .send import send_message

# All method names and their functions
STATUSES: Dict[str, Callable[[JSONDict, Any], Union[JSONDict, bool]]] = {
    "getMe": get_me,
    "deleteWebhook": delete_webhook,
    "getUpdates": get_updates,
    "sendMessage": send_message
}
