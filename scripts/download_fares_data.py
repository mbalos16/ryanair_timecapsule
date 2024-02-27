"""
usage: 
python download_fares_data.py \
    --depart-iata-code STN \
    --depart-date-from 2024-10-08 \
    --depart-date-to 2024-11-15 \
    --depart-time-from 06:00 \
    --depart-time-to 00:00 \
    --duration-from 1 \
    --duration-to 4  \
    --n-passangers 1 \
    --market en-gb \
    --out-dir /Users/maria/Desktop/Ryanair/
"""

import argparse
import json
import os
from datetime import datetime

from ryanair_timecapsule.api.fare_finder import Params, get_flights_fares


def parse_args():
    params = argparse.ArgumentParser(
        usage=(
            "This script is intended to access the fare_finder API and store Ryanair information."
        )
    )

    params.add_argument(
        "--depart-iata-code",
        required=True,
        type=str,
        help="The IATA code of the departure country.",
    )

    params.add_argument(
        "--depart-date-from",
        required=True,
        type=str,
        help="Start date of the flight search in ISO format. E.g. 2024-10-24",
    )

    params.add_argument(
        "--depart-date-to",
        required=True,
        type=str,
        help="End date of the flight search in ISO format. E.g. 2024-11-24",
    )

    params.add_argument(
        "--depart-time-from",
        default=Params.model_fields["outboundDepartureTimeFrom"].default,
        type=str,
        help="The departure time from, format HH:MM. By default",
    )

    params.add_argument(
        "--depart-time-to",
        default=Params.model_fields["outboundDepartureTimeTo"].default,
        type=str,
        help="The departure time to, format HH:MM.",
    )

    params.add_argument(
        "--duration-from",
        default=0.01,
        type=float,
        help="Minimum flight time in hours.",
    )

    params.add_argument(
        "--duration-to",
        default=24,
        type=float,
        help="Maximum flight time in hours.",
    )

    params.add_argument(
        "--n-passangers",
        default=Params.model_fields["adultPaxCount"].default,
        type=int,
        help="Number of passangers.",
    )

    params.add_argument(
        "--market",
        default=Params.model_fields["market"].default,
        type=str,
        help="ISO language codes. E.g. en-gb",
    )

    params.add_argument(
        "--out-dir",
        required=True,
        type=str,
        help=(
            "Path to the directory where the requested results will be saved in JSON format."
        ),
    )

    params.add_argument(
        "--debug",
        action="store_true",
        help=("If provided, the script is run in debug mode, i.e. no API call."),
    )
    return params.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if not os.path.exists(args.out_dir):
        exception_message = f"The path '{args.out_dir}' is not a valid path."
        raise ValueError(exception_message)

    result = get_flights_fares(
        depart_iata_code=args.depart_iata_code,
        depart_date_from=args.depart_date_from,
        depart_date_to=args.depart_date_to,
        duration_from=args.duration_from,
        duration_to=args.duration_to,
        depart_time_from=args.depart_time_from,
        depart_time_to=args.depart_time_to,
        n_passengers=args.n_passangers,
        market=args.market,
    )

    now = datetime.now().isoformat()
    file_name = f"{now}_{args.depart_iata_code}_FROM-{args.depart_date_from}_TO-{args.depart_date_to}"
    path = os.path.join(args.out_dir, f"{file_name}.json")

    with open(path, "w") as f:
        data = json.dumps(result, indent=4)
        f.write(data)
