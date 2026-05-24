#!/usr/bin/env python3
"""
fetch_country_pm25.py

OpenAQ v3 Country-Level PM2.5 Collector
for the Environmental Cybersecurity Project.

PURPOSE
-------
Fetch PM2.5 measurements for ALL PM2.5 sensors
within a selected country using OpenAQ v3.

CORRECT OPENAQ v3 FLOW
----------------------
Country
    ↓
Locations
    ↓
Location Metadata
    ↓
PM2.5 Sensors
    ↓
Sensor Measurements

TEST COUNTRY
------------
Ethiopia (ET)

RECOMMENDED USAGE
-----------------
export OPENAQ_API_KEY="your_api_key"

python fetch_country_pm25.py \
    --country ET \
    --start-date 2025-01-01 \
    --end-date 2025-01-31
"""

import os
import json
import time
import argparse
import logging

from pathlib import Path
from datetime import datetime

import requests
import pandas as pd

from dotenv import load_dotenv

# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

API_KEY = os.getenv("OPENAQ_API_KEY")

if not API_KEY:
    raise EnvironmentError(
        "OPENAQ_API_KEY environment variable not found."
    )

# ============================================================
# CONFIGURATION
# ============================================================

BASE_URL = "https://api.openaq.org/v3"

RAW_DIR = Path("data/raw/openaq")
PROCESSED_DIR = Path("data/processed")
LOG_DIR = Path("logs")

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "country_pm25_fetch.log"

# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)

console.setFormatter(formatter)

logging.getLogger("").addHandler(console)

# ============================================================
# SESSION
# ============================================================

HEADERS = {
    "X-API-Key": API_KEY
}

session = requests.Session()
session.headers.update(HEADERS)

# ============================================================
# REQUEST HELPER
# ============================================================

def request_with_retries(
        url,
        params=None,
        retries=3,
        backoff=2
):

    for attempt in range(1, retries + 1):

        try:

            response = session.get(
                url,
                params=params,
                timeout=30
            )

            if response.status_code == 200:
                return response.json()

            logging.warning(
                f"HTTP {response.status_code} | "
                f"URL: {url}"
            )

        except requests.RequestException as e:

            logging.warning(
                f"Request failed: {e}"
            )

        sleep_time = backoff ** attempt

        logging.info(
            f"Retrying in {sleep_time}s..."
        )

        time.sleep(sleep_time)

    return None

# ============================================================
# FETCH COUNTRY LOCATIONS
# ============================================================

def fetch_country_locations(country_code):
    """
    Fetch all locations for a country.
    """

    logging.info(
        f"Fetching locations for country: {country_code}"
    )

    all_locations = []

    page = 1

    while True:

        url = f"{BASE_URL}/locations"

        params = {
            "countries": country_code,
            "limit": 100,
            "page": page
        }

        data = request_with_retries(
            url,
            params=params
        )

        if data is None:
            break

        results = data.get("results", [])

        if not results:
            break

        all_locations.extend(results)

        logging.info(
            f"Fetched location page {page} "
            f"({len(results)} rows)"
        )

        page += 1

        time.sleep(1)

    logging.info(
        f"Total locations discovered: "
        f"{len(all_locations)}"
    )

    return all_locations

# ============================================================
# LOCATION METADATA
# ============================================================

def fetch_location_metadata(location_id):
    """
    Fetch detailed location metadata.
    """

    url = f"{BASE_URL}/locations/{location_id}"

    logging.info(
        f"Fetching location metadata: {location_id}"
    )

    data = request_with_retries(url)

    return data

# ============================================================
# SENSOR DISCOVERY
# ============================================================

def extract_pm25_sensors(location_data):
    """
    Extract PM2.5 sensors only.
    """

    sensors = []

    results = location_data.get("results", [])

    if not results:
        return sensors

    location = results[0]

    for sensor in location.get("sensors", []):

        parameter = sensor.get("parameter", {})
        parameter_name = parameter.get(
            "name",
            ""
        ).lower()

        sensor_name = sensor.get(
            "name",
            ""
        ).lower()

        if (
            parameter_name == "pm25"
            or "pm25" in sensor_name
        ):

            sensors.append({

                "sensor_id":
                    sensor.get("id"),

                "sensor_name":
                    sensor.get("name"),

                "parameter":
                    parameter_name,

                "units":
                    parameter.get("units")
            })

    return sensors

# ============================================================
# FETCH SENSOR MEASUREMENTS
# ============================================================

def fetch_measurements(
        sensor_id,
        start_date,
        end_date,
        limit=1000
):
    """
    Fetch measurements from sensor endpoint.
    """

    logging.info(
        f"Fetching measurements for sensor "
        f"{sensor_id}"
    )

    all_results = []

    page = 1

    while True:

        url = (
            f"{BASE_URL}/sensors/"
            f"{sensor_id}/measurements"
        )

        params = {

            "date_from":
                f"{start_date}T00:00:00Z",

            "date_to":
                f"{end_date}T23:59:59Z",

            "limit":
                limit,

            "page":
                page
        }

        data = request_with_retries(
            url,
            params=params
        )

        if data is None:
            break

        results = data.get("results", [])

        if not results:
            break

        all_results.extend(results)

        logging.info(
            f"Sensor {sensor_id} | "
            f"Page {page} | "
            f"Rows: {len(results)}"
        )

        page += 1

        time.sleep(1)

    logging.info(
        f"Total measurements collected: "
        f"{len(all_results)}"
    )

    return all_results

# ============================================================
# SAVE RAW JSON
# ============================================================

def save_raw_json(data, filename):

    output_path = RAW_DIR / filename

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    logging.info(
        f"Saved raw JSON: {output_path}"
    )

# ============================================================
# NORMALIZE DATAFRAME
# ============================================================

def normalize_measurements(
        measurements,
        metadata,
        sensor_info
):
    """
    Normalize OpenAQ response into dataframe.
    """

    records = []

    location = metadata["results"][0]

    coordinates = location.get(
        "coordinates",
        {}
    )

    for row in measurements:

        records.append({

            "timestamp_utc":
                row.get("period", {})
                   .get("datetimeFrom", {})
                   .get("utc"),

            "timestamp_local":
                row.get("period", {})
                   .get("datetimeFrom", {})
                   .get("local"),

            "value":
                row.get("value"),

            "parameter":
                sensor_info["parameter"],

            "units":
                sensor_info["units"],

            "sensor_id":
                sensor_info["sensor_id"],

            "sensor_name":
                sensor_info["sensor_name"],

            "location_id":
                location.get("id"),

            "location_name":
                location.get("name"),

            "country":
                location.get("country", {})
                        .get("name"),

            "provider":
                location.get("provider", {})
                        .get("name"),

            "owner":
                location.get("owner", {})
                        .get("name"),

            "latitude":
                coordinates.get("latitude"),

            "longitude":
                coordinates.get("longitude")
        })

    df = pd.DataFrame(records)

    if df.empty:
        return df

    # ========================================================
    # CLEANING
    # ========================================================

    df["timestamp_utc"] = pd.to_datetime(
        df["timestamp_utc"],
        utc=True,
        errors="coerce"
    )

    df = df.dropna(
        subset=["timestamp_utc", "value"]
    )

    # Remove impossible PM2.5 values
    df = df[df["value"] >= 0]

    # Remove duplicates
    df = df.drop_duplicates()

    # Sort chronologically
    df = df.sort_values("timestamp_utc")

    return df

# ============================================================
# EXPORT CSV
# ============================================================

def export_csv(df, filename):

    output_path = PROCESSED_DIR / filename

    df.to_csv(output_path, index=False)

    logging.info(
        f"Saved processed CSV: {output_path}"
    )

# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description="Country-level OpenAQ PM2.5 collector"
    )

    parser.add_argument(
        "--country",
        default="ET",
        help="ISO country code (default: ET)"
    )

    parser.add_argument(
        "--start-date",
        default="2025-01-01",
        help="Start date YYYY-MM-DD"
    )

    parser.add_argument(
        "--end-date",
        default="2025-01-07",
        help="End date YYYY-MM-DD"
    )

    args = parser.parse_args()

    country_code = args.country.upper()
    start_date = args.start_date
    end_date = args.end_date

    logging.info("===================================")
    logging.info("OpenAQ Country PM2.5 Collector")
    logging.info("===================================")

    logging.info(f"Country     : {country_code}")
    logging.info(f"Start Date  : {start_date}")
    logging.info(f"End Date    : {end_date}")

    # ========================================================
    # STEP 1 — COUNTRY LOCATIONS
    # ========================================================

    locations = fetch_country_locations(
        country_code
    )

    if not locations:

        logging.warning(
            "No locations discovered."
        )

        return

    all_dataframes = []

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    # ========================================================
    # STEP 2 — LOCATION LOOP
    # ========================================================

    for location in locations:

        location_id = location.get("id")

        logging.info(
            f"Processing location "
            f"{location_id}"
        )

        # ----------------------------------------------------
        # FETCH FULL LOCATION METADATA
        # ----------------------------------------------------

        metadata = fetch_location_metadata(
            location_id
        )

        if metadata is None:
            continue

        # ----------------------------------------------------
        # EXTRACT PM2.5 SENSORS
        # ----------------------------------------------------

        sensors = extract_pm25_sensors(
            metadata
        )

        if not sensors:

            logging.info(
                f"No PM2.5 sensors found "
                f"for location {location_id}"
            )

            continue

        logging.info(
            f"Discovered {len(sensors)} "
            f"PM2.5 sensor(s)"
        )

        # ----------------------------------------------------
        # SENSOR LOOP
        # ----------------------------------------------------

        for sensor in sensors:

            sensor_id = sensor["sensor_id"]

            measurements = fetch_measurements(
                sensor_id,
                start_date,
                end_date
            )

            if not measurements:

                logging.warning(
                    f"No measurements returned "
                    f"for sensor {sensor_id}"
                )

                continue

            # ------------------------------------------------
            # SAVE RAW JSON
            # ------------------------------------------------

            raw_filename = (
                f"{country_code}_"
                f"sensor_{sensor_id}_"
                f"{timestamp}.json"
            )

            save_raw_json(
                measurements,
                raw_filename
            )

            # ------------------------------------------------
            # NORMALIZE
            # ------------------------------------------------

            df = normalize_measurements(
                measurements,
                metadata,
                sensor
            )

            if df.empty:

                logging.warning(
                    f"Empty dataframe for "
                    f"sensor {sensor_id}"
                )

                continue

            all_dataframes.append(df)

            logging.info(
                f"Normalized rows: {len(df)}"
            )

    # ========================================================
    # FINAL EXPORT
    # ========================================================

    if not all_dataframes:

        logging.warning(
            "No PM2.5 data collected."
        )

        return

    final_df = pd.concat(
        all_dataframes,
        ignore_index=True
    )

    final_df = final_df.drop_duplicates()

    final_df = final_df.sort_values(
        "timestamp_utc"
    )

    csv_filename = (
        f"{country_code.lower()}_pm25_"
        f"{start_date}_to_{end_date}.csv"
    )

    export_csv(
        final_df,
        csv_filename
    )

    logging.info("===================================")
    logging.info("Collection completed successfully")
    logging.info("===================================")

    print(final_df.head())
    print(f"\nTotal rows: {len(final_df)}")

# ============================================================
# ENTRYPOINT
# ============================================================

if __name__ == "__main__":
    main()