import requests
from requests.models import Response


def call_api(
    url: str, params: dict = None, return_json: bool = True
) -> dict | Response:
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    if return_json:
        return response.json()
    return response
