import re
from datetime import date, time

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
    ToUs: str = Field(default="AGREED")  # Terms of use
    RoundTrip: bool = Field(default=False)

    @field_validator("DateOut", "DateIn")
    def check_date(cls, value):
        try:
            date.fromisoformat(value)
        except:
            raise ValueError(f"The date {value} needs to be in format YYYY-MM-DD.")
        return value


# Authentication
def get_auth() -> tuple:
    response = utils.call_api(url=AUTH_ENDPOINT, return_json=False)
    cookies = response.headers["Set-Cookie"]
    if "rid=" not in cookies or "rid.sig=" not in cookies:
        raise ValueError(
            "Authentication ids ('rid' and 'rid.sig') not found in response headers."
        )
    rid = re.match(r".*rid=(.+?)[;, ].*", cookies)
    if not rid:
        raise ValueError("'rid' not found among cookies.")
    rid = rid.group(1)
    rid_sig = re.match(r".*rid\.sig=(.+?)[;, ].*", cookies)

    if not rid_sig:
        raise ValueError("'rid.sig' not found among cookies.")
    rid_sig = rid_sig.group(1)
    return rid, rid_sig


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
        RoundTrip=False,
        ToUs="AGREED",
    )

    api_params = parameters.model_dump()
    rid, rid_sig = get_auth()
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0",
        "Cookie": f"rid={rid};rid.sig={rid_sig}",
        "TE": "trailers",
        "Pragma": "no-cache",
    }

    return utils.call_api(
        url=ENDPOINT, params=api_params, return_json=True, headers=headers
    )
