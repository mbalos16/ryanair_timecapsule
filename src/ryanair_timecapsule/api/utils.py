import requests
from requests.models import Response


def call_api(
    url: str, params: dict = None, return_json: bool = True, headers: dict = None
) -> dict | Response:
    response = requests.get(url=url, params=params, headers=headers)
    response.raise_for_status()
    if return_json:
        return response.json()
    return response
