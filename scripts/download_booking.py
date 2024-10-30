"""
usage: 
python download_booking.py \
    --depart-iata-code STN \
    --destination-iata-code VLC \
    --depart-date-from 2024-10-25 \
    --depart-date-to 2024-11-10 \
    --n-adults 1 \
    --n-teenagers 0 \
    --n-children 0 \
    --n-infants 0 \ 
    --out-dir ../test
"""

import argparse
import json
import os
from datetime import datetime

from ryanair_timecapsule.api.booking import Params, get_flights_booking


def parse_args():
    params = argparse.ArgumentParser(
        usage=(
            "This script is intended to access the booking API and store Ryanair information."
        )
    )

    params.add_argument(
        "--depart-iata-code",
        required=True,
        type=str,
        help="The IATA code of the departure country.",
    )

    params.add_argument(
        "--destination-iata-code",
        required=True,
        type=str,
        help="The IATA code of the destination country.",
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
        "--n-adults",
        default=Params.model_fields["ADT"].default,
        type=int,
        help="Number of adult passangers, aged 16 or over at the time of travel.",
    )

    params.add_argument(
        "--n-teenagers",
        default=Params.model_fields["TEEN"].default,
        type=int,
        help="Number of teenage passengers, aged 12 to 15 years old at the time of travel.",
    )

    params.add_argument(
        "--n-children",
        default=Params.model_fields["CHD"].default,
        type=int,
        help="Number of children passangers, aged 2 to 11 years old at the time of travel.",
    )

    params.add_argument(
        "--n-infants",
        default=Params.model_fields["INF"].default,
        type=int,
        help="Number of  passangers under 2 years old at the time of travel.",
    )

    params.add_argument(
        "--out-dir",
        required=True,
        type=str,
        help=(
            "Path to the directory wh[]ere the requested results will be saved in JSON format."
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

    result = get_flights_booking(
        n_adults=args.n_adults,
        n_teenagers=args.n_teenagers,
        n_children=args.n_children,
        n_infants=args.n_infants,
        depart_iata_code=args.depart_iata_code,
        destination_iata_code=args.destination_iata_code,
        depart_date_from=args.depart_date_from,
        depart_date_to=args.depart_date_to,
    )

    # Save the data
    now = datetime.now().isoformat()
    file_name = f"{now}_{args.depart_iata_code}_FROM-{args.depart_date_from}_TO-{args.depart_date_to}_Booking"
    path = os.path.join(args.out_dir, f"{file_name}.json")

    with open(path, "w") as f:
        data = json.dumps(result, indent=4)
        f.write(data)
