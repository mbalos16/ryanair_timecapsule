import requests

MARKETS_ENDPOINT = "https://www.ryanair.com/content/ryanair.markets.json"
ACTIVE_IATA_ENDPOINT = "https://www.ryanair.com/api/views/locate/5/airports/en/active"

def download_active_market() -> set:
    """Makes a request to a specific URL and returns the active Ryanair market codes

    Returns:
        set: The active Ryanair markets.
    """
    response = requests.get(MARKETS_ENDPOINT).json()
    market_codes = {country["code"] for country in response}
    return market_codes

def download_active_iata_codes() -> set:
    """Makes a request to a specific URL and returns the active Ryanair IATA codes

    Returns:
        set: The active Ryanair IATA codes.
    """
    response = requests.get(ACTIVE_IATA_ENDPOINT).json()
    iata_codes = set([country["code"] for country in response])
    return iata_codes


MARKETS = download_active_market()
IATA_CODES = download_active_iata_codes()