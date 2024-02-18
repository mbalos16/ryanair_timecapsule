import pytest
from pydantic import ValidationError

from ryanair_timecapsule.api.fare_finder import ENDPOINT, get_flights_fares
from ryanair_timecapsule.api.utils import call_api

DEFAULT_PARAMS = {
    "outboundDepartureTimeFrom": "00:00",
    "outboundDepartureTimeTo": "23:59",
    "adultPaxCount": 1,
    "market": "en-gb",
    "searchMode": "ALL",
    "offset": 0,
    "limit": 39999,
}


def mock_call_api(url, params, return_json):
    return url, params, return_json


def test_get_flights_fares_correct_params(monkeypatch):
    monkeypatch.setattr("ryanair_timecapsule.api.utils.call_api", mock_call_api)
    url, params, return_json = get_flights_fares(
        "STN", "2024-03-19", "2024-03-24", 1, 5
    )
    expected_params = DEFAULT_PARAMS.copy()
    expected_params.update(
        {
            "departureAirportIataCode": "STN",
            "outboundDepartureDateFrom": "2024-03-19",
            "outboundDepartureDateTo": "2024-03-24",
            "durationFrom": 1,
            "durationTo": 5,
        }
    )

    # Check Endpoint
    assert url == ENDPOINT

    # Check params
    assert type(params) is dict
    assert params == expected_params


@pytest.mark.parametrize(
    "iata_code,date_from,date_to,duration_from,duration_to,time_from,time_to,n_pass,market",
    # fmt: off
    [
        ("MU", "2024-03-19", "2024-03-24", 1, 5, "00:00", "23:59", 1, "en-gb"),  # wrong iata
        ("STN", "19-03-2024", "2024-03-24", 1, 5, "00:00", "23:59", 1, "en-gb"),  # wrong date from
        ("STN", "2024-03-19", "24-03-2024", 1, 5, "00:00", "23:59", 1, "en-gb"),  # wrong date to
        ("STN", "2024-03-19", "2024-03-24", 0, 5, "00:00", "23:59", 1, "en-gb"),  # wrong duration from
        ("STN", "2024-03-19", "2024-03-24", 1, 0, "00:00", "23:59", 1, "en-gb"),  # wrong duration to
        ("STN", "2024-03-19", "2024-03-24", 1, 5, "00:62", "23:59", 1, "en-gb"),  # wrong time from 
        ("STN", "2024-03-19", "2024-03-24", 1, 5, "00:00", "27:59", 1, "en-gb"),   # wrong time to
        ("STN", "2024-03-19", "2024-03-24", 1, 5, "00:00", "23:59", 0, "en-gb"),  # wrong number pass
        ("STN", "2024-03-19", "2024-03-24", 1, 5, "00:00", "23:59", 1, "en-uk"),  # wrong market
    ],
    # fmt: on
)
def test_get_flights_fares_incorrect_params(
    monkeypatch,
    iata_code,
    date_from,
    date_to,
    duration_from,
    duration_to,
    time_from,
    time_to,
    n_pass,
    market,
):
    monkeypatch.setattr("ryanair_timecapsule.api.utils.call_api", mock_call_api)
    with pytest.raises(ValidationError):
        url, params, return_json = get_flights_fares(
            iata_code,
            date_from,
            date_to,
            duration_from,
            duration_to,
            time_from,
            time_to,
            n_pass,
            market,
        )
