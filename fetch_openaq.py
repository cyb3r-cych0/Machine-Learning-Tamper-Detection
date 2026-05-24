#!/usr/bin/env python3
"""
fetch_openaq.py

Research-grade OpenAQ v3 data collection pipeline
for the Environmental Cybersecurity project.

Purpose:
    - Fetch OpenAQ v3 location metadata
    - Discover PM2.5 sensors dynamically
    - Download paginated measurement data
    - Preserve immutable raw JSON
    - Export cleaned CSV datasets
    - Log collection activity for reproducibility

Author:
    Environmental Cybersecurity Project

Recommended Usage:
    export OPENAQ_API_KEY="your_api_key"

    python fetch_openaq.py \
        --location-id 8118 \
        --start-date 2025-01-01 \
        --end-date 2025-12-31
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

load_dotenv()

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

LOG_FILE = LOG_DIR / "openaq_fetch.log"

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
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
console.setFormatter(formatter)

logging.getLogger("").addHandler(console)

# ============================================================
# API SESSION
# ============================================================

API_KEY = os.getenv("OPENAQ_API_KEY")

if not API_KEY:
    raise EnvironmentError(
        "OPENAQ_API_KEY environment variable not found."
    )

HEADERS = {
    "X-API-Key": API_KEY
}

session = requests.Session()
session.headers.update(HEADERS)

# ============================================================
# HELPERS
# ============================================================

def request_with_retries(
        url,
        params=None,
        retries=1,
        backoff=2
):
    """
    Robust GET request handler with:
        - retry logic
        - graceful degradation
        - rate limit awareness
        - timeout handling
    """

    for attempt in range(1, retries + 1):

        try:

            response = session.get(
                url,
                params=params,
                timeout=30
            )

            # ====================================================
            # RATE LIMIT HEADERS
            # ====================================================

            limit_header = response.headers.get(
                "x-ratelimit-limit"
            )

            remaining_header = response.headers.get(
                "x-ratelimit-remaining"
            )

            reset_header = response.headers.get(
                "x-ratelimit-reset"
            )

            limit = int(limit_header) if limit_header else None
            remaining = int(remaining_header) if remaining_header else None
            reset = int(reset_header) if reset_header else 60

            # ====================================================
            # LOG RATE LIMITS
            # ====================================================

            if limit is not None and remaining is not None:

                logging.info(
                    f"Rate Limit: "
                    f"{remaining}/{limit} remaining"
                )

            # ====================================================
            # SUCCESS
            # ====================================================

            if response.status_code == 200:
                return response.json()

            # ====================================================
            # RATE LIMITED
            # ====================================================

            if response.status_code == 429:

                logging.warning(
                    "API rate limit exceeded."
                )

                user_choice = input(
                    "\n[WARNING] API rate limit exceeded.\n"
                    "1 - Wait and continue\n"
                    "2 - Stop and preserve partial data\n"
                    "\nEnter choice: "
                ).strip()

                if user_choice == "1":

                    wait_time = reset + 1

                    logging.warning(
                        f"Sleeping for {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

                else:

                    logging.warning(
                        "Stopping collection gracefully."
                    )

                    return None

            # ====================================================
            # SERVER TIMEOUTS
            # ====================================================

            if response.status_code == 408:

                logging.warning(
                    f"HTTP 408 timeout "
                    f"(attempt {attempt}/{retries})"
                )

                if attempt >= retries:

                    logging.warning(
                        "Maximum retries reached. "
                        "Proceeding with partial data."
                    )

                    return None

            # ====================================================
            # OTHER HTTP ERRORS
            # ====================================================

            else:

                logging.warning(
                    f"HTTP {response.status_code} "
                    f"for {url}"
                )

                if attempt >= retries:

                    logging.warning(
                        "Maximum retries reached. "
                        "Proceeding with partial data."
                    )

                    return None

        except requests.RequestException as e:

            logging.warning(
                f"Request failed: {e}"
            )

            if attempt >= retries:

                logging.warning(
                    "Maximum retries reached. "
                    "Proceeding with partial data."
                )

                return None

        # ========================================================
        # RETRY BACKOFF
        # ========================================================

        sleep_time = backoff ** attempt

        logging.info(
            f"Retrying in {sleep_time}s..."
        )

        time.sleep(sleep_time)

    return None

# ============================================================
# LOCATION METADATA
# ============================================================

def fetch_location_metadata(location_id):
    """
    Fetch OpenAQ location metadata.
    """

    url = f"{BASE_URL}/locations/{location_id}"

    logging.info(f"Fetching location metadata: {location_id}")

    data = request_with_retries(url)

    return data


# ============================================================
# SENSOR DISCOVERY
# ============================================================

def extract_pm25_sensors(location_data):
    """
    Dynamically discover PM2.5 sensors.
    """

    sensors = []

    results = location_data.get("results", [])

    if not results:
        raise ValueError("No location results returned.")

    location = results[0]

    for sensor in location.get("sensors", []):

        sensor_name = sensor.get("name", "").lower()

        parameter = sensor.get("parameter", {})
        parameter_name = parameter.get("name", "").lower()

        if parameter_name == "pm25" or "pm25" in sensor_name:
            sensors.append({
                "sensor_id": sensor["id"],
                "sensor_name": sensor["name"],
                "parameter": parameter_name,
                "units": parameter.get("units")
            })

    return sensors


# ============================================================
# MEASUREMENT COLLECTION
# ============================================================

def fetch_measurements(sensor_id, start_date, end_date, limit=1000):
    """
    Fetch paginated measurements for a sensor.
    """

    logging.info(f"Fetching measurements for sensor {sensor_id}")

    all_results = []
    page = 1

    while True:

        url = f"{BASE_URL}/sensors/{sensor_id}/measurements"

        params = {
            "date_from": f"{start_date}T00:00:00Z",
            "date_to": f"{end_date}T23:59:59Z",
            "limit": limit,
            "page": page
        }

        data = request_with_retries(url, params=params)

        # ========================================================
        # GRACEFUL FAILURE
        # ========================================================

        if data is None:
            logging.warning(
                "Stopping pagination early due to "
                "request failures."
            )

            break

        results = data.get("results", [])

        if not results:
            break

        all_results.extend(results)

        logging.info(
            f"Fetched page {page} "
            f"({len(results)} rows)"
        )

        page += 1

        time.sleep(1)

    logging.info(
        f"Total measurements collected: {len(all_results)}"
    )

    return all_results


# ============================================================
# RAW JSON STORAGE
# ============================================================

def save_raw_json(data, filename):
    """
    Preserve immutable raw API responses.
    """

    output_path = RAW_DIR / filename

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    logging.info(f"Saved raw JSON: {output_path}")


# ============================================================
# DATAFRAME NORMALIZATION
# ============================================================

def normalize_measurements(
    measurements,
    metadata,
    sensor_info
):
    """
    Convert API results into clean analytical dataframe.
    """

    records = []

    location = metadata["results"][0]

    coordinates = location.get("coordinates", {})

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

            "location_id":
                location.get("id"),

            "location_name":
                location.get("name"),

            "country":
                location.get("country", {}).get("name"),

            "provider":
                location.get("provider", {}).get("name"),

            "owner":
                location.get("owner", {}).get("name"),

            "latitude":
                coordinates.get("latitude"),

            "longitude":
                coordinates.get("longitude")
        })

    df = pd.DataFrame(records)

    # ========================================================
    # CLEANING
    # ========================================================

    df["timestamp_utc"] = pd.to_datetime(
        df["timestamp_utc"],
        utc=True,
        errors="coerce"
    )

    df = df.dropna(subset=["timestamp_utc", "value"])

    # Remove impossible negative PM2.5 values
    df = df[df["value"] >= 0]

    # Remove duplicates
    df = df.drop_duplicates()

    # Sort chronologically
    df = df.sort_values("timestamp_utc")

    return df


# ============================================================
# CSV EXPORT
# ============================================================

def export_csv(df, filename):
    """
    Export processed analytical dataset.
    """

    output_path = PROCESSED_DIR / filename

    df.to_csv(output_path, index=False)

    logging.info(f"Saved processed CSV: {output_path}")


# ============================================================
# MAIN PIPELINE
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description="OpenAQ v3 PM2.5 data collector"
    )

    parser.add_argument(
        "--location-id",
        type=int,
        default=8118,
        help="OpenAQ location ID (default: 8118)"
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

    location_id = args.location_id
    start_date = args.start_date
    end_date = args.end_date

    logging.info("===================================")
    logging.info("OpenAQ Environmental Data Collector")
    logging.info("===================================")

    logging.info(f"Location ID : {location_id}")
    logging.info(f"Start Date  : {start_date}")
    logging.info(f"End Date    : {end_date}")

    # ========================================================
    # STEP 1 — LOCATION METADATA
    # ========================================================

    metadata = fetch_location_metadata(location_id)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    raw_meta_file = (
        f"location_{location_id}_metadata_{timestamp}.json"
    )

    save_raw_json(metadata, raw_meta_file)

    # ========================================================
    # STEP 2 — SENSOR DISCOVERY
    # ========================================================

    sensors = extract_pm25_sensors(metadata)

    if not sensors:
        raise RuntimeError(
            "No PM2.5 sensors discovered."
        )

    logging.info(
        f"Discovered {len(sensors)} PM2.5 sensor(s)"
    )

    # ========================================================
    # STEP 3 — FETCH MEASUREMENTS
    # ========================================================

    for sensor in sensors:

        sensor_id = sensor["sensor_id"]

        logging.info(
            f"Processing sensor: {sensor_id}"
        )

        measurements = fetch_measurements(
            sensor_id,
            start_date,
            end_date
        )

        if not measurements:
            logging.warning(
                f"No measurements returned for sensor {sensor_id}"
            )
            continue

        # ====================================================
        # SAVE RAW JSON
        # ====================================================

        raw_measurement_file = (
            f"sensor_{sensor_id}_measurements_{timestamp}.json"
        )

        save_raw_json(
            measurements,
            raw_measurement_file
        )

        # ====================================================
        # NORMALIZE DATA
        # ====================================================

        df = normalize_measurements(
            measurements,
            metadata,
            sensor
        )

        logging.info(
            f"Normalized dataframe rows: {len(df)}"
        )

        # ====================================================
        # EXPORT CSV
        # ====================================================

        location_name = (
            metadata["results"][0]["name"]
            .lower()
            .replace(" ", "_")
        )

        csv_name = (
            f"{location_name}_pm25_"
            f"{start_date}_to_{end_date}.csv"
        )

        export_csv(df, csv_name)

        logging.info(
            f"Completed sensor {sensor_id}"
        )

    logging.info("===================================")
    logging.info("Pipeline completed successfully.")
    logging.info("===================================")


# ============================================================
# ENTRYPOINT
# ============================================================

if __name__ == "__main__":
    main()