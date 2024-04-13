# Ryanair timecapsule

This project is a reverse-engineering of the Ryanair API that allows collecting daily prices of flights. The [Fare-Finder Ryanair](https://www.ryanair.com/gb/en/cheap-flights) API is already implemented, and the Booking API is the next one on my list.

The goal of this tool is to collect data to feed machine learning models to forecast Ryanair prices, as a personal project. Please feel free to fork or contribute to this project. Keep in mind this is a personal project, feedback is more than welcome.

## Getting started

Please follow the next steps to call the API in your system:

### Setup

1. Open a terminal and clone the repository using: `git clone https://github.com/mbalos16/ryanair_timecapsule.git`
2. Navigate to the cloned folder using the `cd` command.
3. Create a new python environment using the following command: `python -m venv .venv`
4. Activate the python environment with `source .venv/bin/activate`
5. Install the requirements by using `pip install -r requirements.txt`

### Fare-Finder API call example

```
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
    --out-dir <output-directory>
```

## Contribution

Pull requests and issues are welcome.

## Licence

This repository is licensed under CC0. More info in the [LICENSE](./LICENSE) file.

Copyright (c) 2024 Maria Magdalena Balos
