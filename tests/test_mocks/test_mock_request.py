from ptbtest.mocks.mock_request import MockRequest
from ptbtest.mocks.mock_server import MockServer
import pytest
from ptbtest import MockUpdater


normal_request = MockRequest()
class TestNormalMockUpdater:
    @pytest.mark.parametrize(
        ("method_name", "method_type"),
        (
            ('server', MockServer), 
        )
    )
    def test_attribute_types(self, method_name, method_type):
        assert hasattr(normal_request, method_name)
        assert isinstance(
            getattr(normal_request, method_name), 
            method_type
        )
