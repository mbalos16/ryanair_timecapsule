import pytest
import requests
from pydantic import ValidationError

from ryanair_timecapsule.api.booking import ENDPOINT, get_flights_booking


def mock_call_api(url, params, headers, return_json):
    if not return_json:
        response = requests.models.Response()
        response.cookies.set("rid", "fake_rid")
        response.cookies.set("rid.sig", "fake_rid_sig")
        return response
    return url, params, headers, return_json


def test_get_booking_correct_params(monkeypatch):
    monkeypatch.setattr("ryanair_timecapsule.api.utils.call_api", mock_call_api)
    url, params, headers, return_json = get_flights_booking(
        n_adults=1,
        n_children=0,
        n_infants=0,
        n_teenagers=0,
        depart_iata_code="STN",
        destination_iata_code="VLC",
        depart_date_from="2024-10-29",
        depart_date_to="2024-10-31",
    )

    expected_params = {
        "ADT": 1,
        "TEEN": 0,
        "CHD": 0,
        "INF": 0,
        "Origin": "STN",
        "Destination": "VLC",
        "DateOut": "2024-10-29",
        "DateIn": "2024-10-31",
        "ToUs": "AGREED",
        "RoundTrip": "true",
        "promoCode": "",
        "IncludeConnectingFlights": "false",
        "FlexDaysBeforeOut": 2,
        "FlexDaysOut": 2,
        "FlexDaysBeforeIn": 2,
        "FlexDaysIn": 2,
        "IncludePrimeFares": "false",
    }

    # Check Endpoint
    assert url == ENDPOINT

    # Check headers
    assert type(headers) is dict

    # Check params
    assert type(params) is dict

    assert params == expected_params


@pytest.mark.parametrize(
    "n_adults, n_teenagers, n_children, n_infants, depart_iata_code, destination_iata_code, depart_date_from, depart_date_to",
    # fmt: off
    [
        (1, 0, 0, 0, "NU", "VLC", "2024-10-30",  "2024-11-10"),  # wrong depart_iata_code
        (1, 0, 0, 0, "STN", "NU", "2024-10-30",  "2024-11-10"),  # wrong destination_iata_code
        (1, 0, 0, 0, "STN", "VLC", "30-10-2024",  "2024-11-10"),  # wrong depart_date_from
        (1, 0, 0, 0, "STN", "VLC", "30-2024-10",  "2024-11-10"),  # wrong depart_date_from
        (1, 0, 0, 0, "STN", "VLC", "2024-10-30",  "10-11-2024"),  # wrong depart_date_to
        (1, 0, 0, 0, "STN", "VLC", "2024-10-30",  "10-2024-11"),  # wrong depart_date_from
    ],
    # fmt: on
)
def test_get_booking_incorrect_params(
    monkeypatch,
    n_adults,
    n_teenagers,
    n_children,
    n_infants,
    depart_iata_code,
    destination_iata_code,
    depart_date_from,
    depart_date_to,
):

    monkeypatch.setattr("ryanair_timecapsule.api.utils.call_api", mock_call_api)
    with pytest.raises(ValidationError):
        url, params, headers, return_json = get_flights_booking(
            n_adults=n_adults,
            n_teenagers=n_teenagers,
            n_children=n_children,
            n_infants=n_infants,
            depart_iata_code=depart_iata_code,
            destination_iata_code=destination_iata_code,
            depart_date_from=depart_date_from,
            depart_date_to=depart_date_to,
        )
