import requests
from requests.models import Response
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503])
session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=retry))


def call_api(
    url: str, params: dict = None, return_json: bool = True, headers: dict = None
) -> dict | Response:
    response = session.get(url=url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    if return_json:
        return response.json()
    return response
