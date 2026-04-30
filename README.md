# Ryanair timecapsule

This project is a reverse-engineering of the Ryanair API that allows collecting daily prices of flights. There are two API Endpoints supported:
- [Fare-Finder Ryanair API](https://www.ryanair.com/gb/en/cheap-flights): where you can query all flights departing or arriving to a specific airport in a range of dates.
- [Booking API](https://www.ryanair.com/gb/en): where you can query all the flights departing from a specified airport and arriving to another specified airport in a range of dates. 

Note that I have found that the prices between the two APIs differ in rare cases. The most trustable source being the Booking API, as it is the one used one booking in the Ryanair website.

The goal of this tool is to collect data to feed machine learning models to forecast Ryanair prices. Please feel free to fork or contribute to this project. Keep in mind this is a personal project, feedback is more than welcome.

## Getting started

Please follow the next steps to call the Fare-Finder API or the Booking API in your system:

### Setup

1. Open a terminal and clone the repository using: `git clone https://github.com/mbalos16/ryanair_timecapsule.git`
2. Navigate to the cloned folder using the `cd` command.
3. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if you don't have it already.

### Fare-Finder API call example

```
uv run python scripts/download_fares_data.py \
    --depart-iata-code STN \
    --depart-date-from 2024-10-08 \
    --depart-date-to 2024-11-15 \
    --depart-time-from 06:00 \
    --depart-time-to 23:59 \
    --duration-from 1 \
    --duration-to 4  \
    --n-passengers 1 \
    --market en-gb \
    --out-dir <output-directory>
```

### Booking API call example

```
uv run python scripts/download_booking.py \
    --depart-iata-code STN \
    --destination-iata-code VLC \
    --depart-date-from 2024-10-25 \
    --depart-date-to 2024-11-10 \
    --n-adults 1 \
    --n-teenagers 0 \
    --n-children 0 \
    --n-infants 0 \
    --out-dir <output-directory>
```
## Contribution

Pull requests and issues are welcome.

## Licence

This repository is licensed under CC0. More info in the [LICENSE](./LICENSE) file.

Copyright (c) 2026 Maria Magdalena Balos