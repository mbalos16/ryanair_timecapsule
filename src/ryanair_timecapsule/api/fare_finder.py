from datetime import date, time

from pydantic import BaseModel, Field, validator

from . import utils
from .constants import MARKETS

ENDPOINT = "https://www.ryanair.com/api/farfnd/3/oneWayFares"


class Params(BaseModel, extra="forbid"):
    departureAirportIataCode: str = Field(min_length=3, max_length=3)
    outboundDepartureDateFrom: str
    outboundDepartureDateTo: str
    outboundDepartureTimeFrom: str = Field(default="00:00")
    outboundDepartureTimeTo: str = Field(default="23:59")
    durationFrom: float | int = Field(gt=0)
    durationTo: float | int = Field(gt=0)
    adultPaxCount: int = Field(default=1, ge=1)
    market: str = Field(default="en-gb")
    searchMode: str = Field(default="ALL")
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=39999, ge=1)

    @validator("outboundDepartureDateFrom", "outboundDepartureDateTo")
    def check_date(cls, value):
        try:
            date.fromisoformat(value)
        except:
            raise ValueError(f"The date {value} needs to be in format YYYY-MM-DD.")
        return value

    @validator("outboundDepartureTimeFrom", "outboundDepartureTimeTo")
    def check_time(cls, value):
        try:
            time.fromisoformat(value)
        except:
            raise ValueError(f"The time {value} needs to be in format HH:MM.")
        return value

    @validator("market")
    def check_market(cls, value):
        assert (
            value in MARKETS
        ), f"'{value}' not recognized as a valid market: {MARKETS}."
        return value


def get_flights_fares(
    depart_iata_code: str,
    depart_date_from: str,
    depart_date_to: str,
    duration_from: float | int,
    duration_to: float | int,
    depart_time_from: str = Params.model_fields["outboundDepartureTimeFrom"].default,
    depart_time_to: str = Params.model_fields["outboundDepartureTimeTo"].default,
    n_passengers: int = Params.model_fields["adultPaxCount"].default,
    market: str = Params.model_fields["market"].default,
) -> dict:

    parameters = Params(
        departureAirportIataCode=depart_iata_code,
        outboundDepartureDateFrom=depart_date_from,
        outboundDepartureDateTo=depart_date_to,
        outboundDepartureTimeFrom=depart_time_from,
        outboundDepartureTimeTo=depart_time_to,
        durationFrom=duration_from,
        durationTo=duration_to,
        adultPaxCount=n_passengers,
        market=market,
    )
    api_params = parameters.model_dump()
    return utils.call_api(url=ENDPOINT, params=api_params, return_json=True)
