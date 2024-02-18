import requests


def call_api(url, params=None, return_json=True):
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    if return_json:
        return response.json()
    return response
