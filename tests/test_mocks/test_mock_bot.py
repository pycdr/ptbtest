from logging import Logger
from ptbtest.mocks.mock_request import MockRequest
from telegram import Chat, User, Bot, Message
from telegram.utils.deprecate import TelegramDeprecationWarning
from ptbtest import MockBot
import pytest


bot = MockBot(
    "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    User(
        id=123456789, first_name="Mock", 
        is_bot=True, username="mockbot",
        language_code="en"
    )
)


class TestMockBot:
    @pytest.mark.parametrize(
        ("method_name", "method_type"),
        (
            ("token", str),
            ("defaults", type(None)),
            ("base_url", str),
            ("base_file_url", str),
            ("_bot", User),
            ("_commands", (list, type(None))),
            ("private_key", type(None)),
            ("logger", Logger),
            ("_request", MockRequest)
        )
    )
    def test_attribute_types(self, method_name, method_type):
        assert hasattr(bot, method_name)
        assert isinstance(
            getattr(bot, method_name), 
            method_type
        )
    
    def test_message_method(self, monkeypatch):
        message = Message(0, 0, Chat(0, "group"))
        monkeypatch.setattr(Bot, "_message", lambda *_, **__: message)
        assert bot._message(..., ...) is message
        assert bot.request.server.bot_reactions.get_nowait() is message
