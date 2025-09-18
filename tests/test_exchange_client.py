from unittest.mock import Mock

from requests import Response
from requests.adapters import HTTPAdapter

from afp.exchange import ExchangeClient


def test_send_request(monkeypatch):
    fake_response = Response()
    fake_response.status_code = 200
    mock_send = Mock(return_value=fake_response)

    monkeypatch.setattr(HTTPAdapter, "send", mock_send)

    client = ExchangeClient("http://bar/")
    client._send_request("POST", "/orders", api_version=2, data="hello")

    mock_send.assert_called_once()
    request = mock_send.call_args_list[0].args[0]
    assert request.method == "POST"
    assert request.url == "http://bar/v2/orders"
    assert request.body == "hello"
