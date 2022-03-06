from queue import Queue
from threading import Event, Lock
from ptbtest.mocks.mock_request import MockRequest
import pytest
import logging
import string
from ptbtest import MockUpdater, MockBot
from telegram.ext import Dispatcher, JobQueue


normal_updater = MockUpdater()
class TestNormalMockUpdater:
    @pytest.mark.parametrize(
        ("method_name", "method_type"),
        (
            ("logger", logging.Logger),
            ("bot", MockBot),
            ("_request", MockRequest),
            ("job_queue", JobQueue),
            ("update_queue", Queue),
            ("persistence", type(None)),
            ("dispatcher", Dispatcher),
            ("user_sig_handler", type(None)),
            ("last_update_id", int),
            ("running", bool),
            ("is_idle", bool),
            ("httpd", type(None)),
        )
    )
    def test_attribute_types(self, method_name, method_type):
        assert hasattr(normal_updater, method_name)
        assert isinstance(
            getattr(normal_updater, method_name), 
            method_type
        )
