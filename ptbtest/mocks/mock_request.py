from .mock_server import MockServer
from telegram.utils.request import Request
from telegram.utils.types import JSONDict
from typing import Union
from urllib.parse import urlparse

class MockRequest(Request):
    def __init__(self, con_pool_size: int = 1, proxy_url: str = None, urllib3_proxy_kwargs: JSONDict = None, connect_timeout: float = 5, read_timeout: float = 5):
        super().__init__(con_pool_size, proxy_url, urllib3_proxy_kwargs, connect_timeout, read_timeout)
        self.server = MockServer()
    def post(self, url: str, data: JSONDict, timeout: float = None) -> Union[JSONDict, bool]:
        status = urlparse(url)[2].rpartition("/")[2]
        return self.server.post(status, data)
