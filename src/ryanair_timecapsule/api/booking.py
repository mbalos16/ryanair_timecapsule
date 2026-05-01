from datetime import date

from pydantic import BaseModel, Field, field_validator

from . import utils
from .constants import MARKETS

ENDPOINT = "https://www.ryanair.com/api/booking/v4/en-gb/availability"
AUTH_ENDPOINT = "https://www.ryanair.com/gb/en/trip/flights/select?"


class Params(BaseModel, extra="forbid"):
    ADT: int = Field(default=1, ge=1)
    TEEN: int = Field(default=0, ge=0)
    CHD: int = Field(default=0, ge=0)
    INF: int = Field(default=0, ge=0)
    Origin: str = Field(min_length=3, max_length=3)
    Destination: str = Field(min_length=3, max_length=3)
    DateOut: str = Field(max_length=10)
    DateIn: str = Field(max_length=10)
    ToUs: str = Field(default="AGREED")
    RoundTrip: bool = Field(default=True)
    promoCode: str = Field(default="")
    IncludeConnectingFlights: bool = Field(default=False)
    FlexDaysBeforeOut: int = Field(default=2)
    FlexDaysOut: int = Field(default=2)
    FlexDaysBeforeIn: int = Field(default=2)
    FlexDaysIn: int = Field(default=2)
    IncludePrimeFares: bool = Field(default=False)

    @field_validator("DateOut", "DateIn")
    def check_date(cls, value):
        try:
            date.fromisoformat(value)
        except ValueError:
            raise ValueError(f"The date {value} needs to be in format YYYY-MM-DD.")
        return value


# Request the data from booking
def get_flights_booking(
    n_adults: int,
    n_teenagers: int,
    n_children: int,
    n_infants: int,
    depart_iata_code: str,
    destination_iata_code: str,
    depart_date_from: str,
    depart_date_to: str,
) -> dict:

    parameters = Params(
        ADT=n_adults,
        TEEN=n_teenagers,
        CHD=n_children,
        INF=n_infants,
        Origin=depart_iata_code,
        Destination=destination_iata_code,
        DateOut=depart_date_from,
        DateIn=depart_date_to,
        ToUs="AGREED",
    )

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0",
        "Accept": "application/json, text/plain, */*",
        "client": "desktop",
        "client-version": "3.195.0",
        "Referer": f"https://www.ryanair.com/gb/en/trip/flights/select?adults={n_adults}&teens={n_teenagers}&children={n_children}&infants={n_infants}&dateOut={depart_date_from}&dateIn={depart_date_to}&isReturn=true&originIata={depart_iata_code}&destinationIata={destination_iata_code}",
        "TE": "trailers",
        "Pragma": "no-cache",
    }
    auth_params = {
        "adults": n_adults,
        "teens": n_teenagers,
        "children": n_children,
        "infants": n_infants,
        "originIata": depart_iata_code,
        "destinationIata": destination_iata_code,
        "dateOut": depart_date_from,
        "dateIn": depart_date_to,
        "isReturn": "true",
        "discount": 0,
        "promoCode": "",
    }

    auth_response = utils.call_api(
        url=AUTH_ENDPOINT, params=auth_params, return_json=False, headers=headers
    )
    rid = auth_response.cookies.get("rid")
    rid_sig = auth_response.cookies.get("rid.sig")
    if not rid or not rid_sig:
        raise ValueError("'rid' and 'rid.sig' not found among cookies.")

    api_params = {
        k: str(v).lower() if isinstance(v, bool) else v
        for k, v in parameters.model_dump().items()
    }
    return utils.call_api(
        url=ENDPOINT, params=api_params, return_json=True, headers=headers
    )
