import requests
from ryanair_timecapsule.api.fare_finder import get_flights_fares
from datetime import datetime
import json
import tempfile
import tarfile
import os
from glob import glob

ACTIVE_IATA_ENDPOINT = "https://www.ryanair.com/api/views/locate/5/airports/en/active"
OUTPUT_ABS_PATH = "/home/mbalos/Desktop/projects/ryanair_timecapsule"


def download_active_iata_codes() -> set:
    """Makes a request to a specific URL and returns the active Ryanair IATA codes

    Returns:
        set: The active Ryanair IATA codes.
    """
    response = requests.get(ACTIVE_IATA_ENDPOINT).json()
    iata_codes = set([country["code"] for country in response])
    return iata_codes


def make_tarfile(output_filename: str, source_dir: str):
    """Creates a gzipped tar archive that contains a top-level folder mirroring source_dir.

    Args:
        output_filename (str): The path and name of the output file.
        If path is not given, the file will be saved in the current working directory.
        Eg:
        - /home/user/Desktop/compressed_file.tar.gz -> will be located in /home/user/Desktop/ with the name compressed_file.tar.gz
        - backup.tar.gz -> will be located in the same working directory as the one from were the script has been run, under the name backup.tar.gz
        source_dir (str): The path to the source directory.
    """

    # Handle missing source directory
    if not os.path.exists(path=source_dir):
        exception_message = (
            f"{source_dir} does not exist. Please provide a valid source directory."
        )
        raise FileNotFoundError(exception_message)

    # Handle missing output directory
    out_dir, out_filename = os.path.split(output_filename)
    if out_dir:
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

    with tarfile.open(output_filename, "w:gz") as tar:
        # Get all the json files from inside the directory:
        data_paths = glob(os.path.join(source_dir, "*.json"))

        # Write each path separately in the tar file.
        for path in data_paths:
            tar.add(path, arcname=os.path.split(path)[-1])


def download_ryanair(
    iata_codes: set,
    date_from: str,
    date_to: str,
    duration_from: int,
    duration_to: int,
    output_path: str,
):
    """Calls the ryanair farefinders api for each IATA code in iata_codes,
        saves the result of each call in a temporary directory. Once the loop finishes
        the data is compressed and saved in the output path.

    Args:
        iata_codes (set): A set of unique airports IATA codes to be used to call the API.
        date_from (str): The date from when to request the data.
        date_to (str): The date until when to request the data.
        duration_from (int): The minimum time of the flight.
        duration_to (int): The maximum time of the flight.
        output_path (str): Path where the compressed file will be saved.
         If just a filename is given the result will be created in the directory
         where the script has been runed from.
    """

    with tempfile.TemporaryDirectory() as temp_dir_name:
        for iata in iata_codes:
            metadata = {
                "date": datetime.now().strftime("%Y%m%dT%H%M%S"),
                "depart_date_from": date_from,
                "depart_date_to": date_to,
                "duration_from": duration_from,
                "duration_to": duration_to,
            }

            response = get_flights_fares(
                depart_iata_code=iata,
                depart_date_from=date_from,
                depart_date_to=date_to,
                duration_from=duration_from,
                duration_to=duration_to,
            )

            result = {"metadata": metadata, "response": response}

            filename = f"{iata}_{date_from}_{date_to}"
            json_file_path = os.path.join(temp_dir_name, f"{filename}.json")
            with open(json_file_path, "w") as f:
                data = json.dumps(result, indent=4)
                f.write(data)

        make_tarfile(output_filename=output_path, source_dir=temp_dir_name)


if __name__ == "__main__":
    iata_codes = download_active_iata_codes()
    output_path = os.path.join(
        OUTPUT_ABS_PATH,
        "ryanair_timecapsule_results",
        str(datetime.now().year),
        str(datetime.now().month),
        str(datetime.now().day),
        f"{datetime.now().strftime('%H%M%S')}.tar.gz",
    )

    download_ryanair(
        iata_codes=iata_codes,
        date_from="2026-05-07",
        date_to="2026-05-09",
        duration_from=1,
        duration_to=5,
        output_path=output_path,
    )
