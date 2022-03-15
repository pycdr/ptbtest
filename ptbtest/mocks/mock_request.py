"""Mock Server using a Mock Server instead of Telegram API"""
from .mock_server import MockServer
from telegram.utils.request import Request
from telegram.utils.types import JSONDict
from typing import Union
from urllib.parse import urlparse

class MockRequest(Request):
    # needed to fix warning
    __slots__ = ('server', )
    def __init__(self, con_pool_size: int = 1, proxy_url: str = None, urllib3_proxy_kwargs: JSONDict = None, connect_timeout: float = 5, read_timeout: float = 5):
        # normal initialization..!
        super().__init__(con_pool_size, proxy_url, urllib3_proxy_kwargs, connect_timeout, read_timeout)
        # create a mock server to use it instead of telegram API
        self.server: MockServer = MockServer()
    def post(self, url: str, data: JSONDict, timeout: float = None) -> Union[JSONDict, bool]:
        # get method name
        status = urlparse(url)[2].rpartition("/")[2]
        # use mock server
        return self.server.post(status, data)
