import pytest
from pydantic import ValidationError

from ryanair_timecapsule.api.booking import ENDPOINT, get_flights_booking
from ryanair_timecapsule.api.utils import call_api


def mock_call_api(url, params, headers, return_json):
    return url, params, headers, return_json


def test_get_booking_correct_params(monkeypatch):
    authed = False

    def mock_get_auth(*args, **kwargs):
        nonlocal authed
        authed = True
        return "fake_rid", "fake_rid_sig"

    monkeypatch.setattr("ryanair_timecapsule.api.utils.call_api", mock_call_api)
    monkeypatch.setattr("ryanair_timecapsule.api.booking.get_auth", mock_get_auth)
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
        "RoundTrip": False,
        "ToUs": "AGREED",
    }

    # Check Endpoint
    assert url == ENDPOINT

    # Check headers
    assert type(headers) is dict

    # Check params
    assert type(params) is dict

    assert params == expected_params

    assert authed == True


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

    authed = False

    def mock_get_auth(*args, **kwargs):
        nonlocal authed
        authed = True
        return "fake_rid", "fake_rid_sig"

    monkeypatch.setattr("ryanair_timecapsule.api.utils.call_api", mock_call_api)
    monkeypatch.setattr("ryanair_timecapsule.api.booking.get_auth", mock_get_auth)
    with pytest.raises(ValidationError):
        url, params, headers, return_json = get_flights_booking(
            n_adults,
            n_children,
            n_infants,
            n_teenagers,
            depart_iata_code,
            destination_iata_code,
            depart_date_from,
            depart_date_to,
        )
