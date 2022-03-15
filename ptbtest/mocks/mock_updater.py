"""This module contains the class MockUpdater, which is used instead of Updater."""

import logging
from queue import Queue
from threading import Event, Lock, Thread
from typing import Any, List
from telegram import User
from telegram.ext import Dispatcher, JobQueue, Updater
from .mock_request import MockRequest
from .mock_bot import MockBot
import random, string

def generate_random_token():
    left = "".join(map(str, random.choices(string.digits, k=9)))
    right = "".join(map(str, random.choices(string.ascii_letters+string.digits, k=35)))
    return f"{left}:{right}"

class MockUpdater(Updater):
    """
    This class, based on :class:`telegram.Updater`, is an alternative of this class for test cases. 
    it uses :class:`ptbtest.mocks.mock_request.MockRequest` and :class:`ptbtest.MockBot`, instead of 
    :class:`Request` and :class:`MockBot`.

    Args:
        token (:obj:`str`, optional): The bot's token. default is :obj:`None` (random token)
        bot_user (:class:`telegram.User`, optional): The bot's user object. default is :obj:`None`
            (predefined user object)
    
    Attributes:
        bot (:class:`ptbtest.MockBot`): The bot used with this Updater.
        user_sig_handler (:obj:`None`): Not effective in this class!
        update_queue (:obj:`Queue`): Queue for the updates.
        job_queue (:class:`telegram.ext.JobQueue`): Jobqueue for the updater.
        dispatcher (:class:`telegram.ext.Dispatcher`): Dispatcher that handles the updates and
            dispatches them to the handlers.
        running (:obj:`bool`): Indicates if the updater is running.
        persistence (:class:`telegram.ext.BasePersistence`): Optional. The persistence class to
            store data that should be persistent over restarts.
        use_context (:obj:`bool`): Optional. :obj:`True` if using context based callbacks.
    """

    def __init__(self, token: str = None, bot_user: User = None):
        # using mock object to ignore using telegram API and be compatible with unittest:
        self._request: MockRequest = MockRequest()
        self.bot: MockBot = MockBot(
            request = self._request, 
            token = token or generate_random_token(),
            bot_user = bot_user
        )
        # these attributes are not really effective in unittest; set their default values.
        self.logger = logging.getLogger(__name__)
        self.update_queue: Queue = Queue()
        self.job_queue = JobQueue()
        self.__exception_event = Event()
        self.persistence = None
        self.dispatcher = Dispatcher(
            self.bot,
            self.update_queue,
            job_queue=self.job_queue,
            workers=4,
            exception_event=self.__exception_event,
            persistence=None,
            use_context=True,
            context_types=None,
        )
        self.job_queue.set_dispatcher(self.dispatcher)
        self.user_sig_handler = None
        self.last_update_id = 0
        self.running = False
        self.is_idle = False
        self.httpd = None
        self.__lock = Lock()
        self.__threads: List[Thread] = []
    
    def __getattribute__(self, __name: str) -> Any:
        # need to fix "AttributeError: self._Updater__lock"
        if __name.startswith("_Updater"):
            return object.__getattribute__(self, f"_MockUpdater{__name[8:]}")
        return object.__getattribute__(self, __name)
