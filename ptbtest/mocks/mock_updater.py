import logging
from queue import Queue
from threading import Event, Lock, Thread
from typing import List
from telegram.ext import Dispatcher, JobQueue, Updater
from .mock_request import MockRequest
from .mock_bot import MockBot

class MockUpdater(Updater):
    """Mock Updater based on `telegram.Updater`"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._request = MockRequest()
        self.bot = MockBot(request = self._request)
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
