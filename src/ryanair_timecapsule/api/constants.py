import requests

MARKETS_ENDPOINT = "https://www.ryanair.com/content/ryanair.markets.json"

def download_active_market() -> set:
    """Makes a request to a specific URL and returns the active Ryanair market codes

    Returns:
        set: The active Ryanair markets.
    """
    response = requests.get(MARKETS_ENDPOINT).json()
    market_codes = {country["code"] for country in response}
    return market_codes

MARKETS = download_active_market()
