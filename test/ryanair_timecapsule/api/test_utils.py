import pytest
import requests
import requests_mock
from requests.exceptions import HTTPError

from ryanair_timecapsule.api.utils import call_api


def mock_requests():
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount("mock://", adapter=adapter)
    adapter.register_uri("GET", "mock://test.com/json", text='{"a": "b"}')
    adapter.register_uri("GET", "mock://test.com/txt", text="abcd")
    adapter.register_uri("GET", "mock://test.com/error", status_code=555)
    adapter.register_uri(
        "GET",
        "mock://test.com/headers",
        request_headers={"key": "val"},
        text="Headers received",
    )

    return session.get


def test_call_api_json(monkeypatch):
    monkeypatch.setattr(requests, "get", mock_requests())
    output = call_api(url="mock://test.com/json")
    assert type(output) is dict
    assert output == {"a": "b"}


def test_call_api_text(monkeypatch):
    monkeypatch.setattr(requests, "get", mock_requests())
    output = call_api(url="mock://test.com/txt", return_json=False)
    assert type(output) is requests.models.Response
    assert output.text == "abcd"


def test_call_api_error(monkeypatch):
    monkeypatch.setattr(requests, "get", mock_requests())
    with pytest.raises(HTTPError):
        call_api(url="mock://test.com/error")


def test_call_api_headers(monkeypatch):
    monkeypatch.setattr(requests, "get", mock_requests())
    output = call_api(
        url="mock://test.com/headers", headers={"key": "val"}, return_json=False
    )
    assert output.text == "Headers received"

    # Ensure that an error is raised when the wrong headers are provided
    with pytest.raises(requests_mock.exceptions.NoMockAddress):
        call_api(
            url="mock://test.com/headers",
            headers={"wrong": "headers"},
            return_json=False,
        )

    # Ensure that an error is raised when no headers are provided
    with pytest.raises(requests_mock.exceptions.NoMockAddress):
        call_api(url="mock://test.com/headers", return_json=False)
