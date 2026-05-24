#!/usr/bin/env python3
"""
check_rate_limit.py

Utility script for monitoring OpenAQ v3 API rate limits.

Purpose:
    - Verify API key validity
    - Inspect current rate limit usage
    - Display remaining requests
    - Estimate collection safety
    - Support research-grade ingestion planning

Usage:
    export OPENAQ_API_KEY="your_api_key"

    python check_rate_limit.py
"""

import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.openaq.org/v3/locations/8118"

API_KEY = os.getenv("OPENAQ_API_KEY")

if not API_KEY:
    raise EnvironmentError(
        "OPENAQ_API_KEY environment variable not found."
    )

HEADERS = {
    "X-API-Key": API_KEY
}


def print_rate_limit_info(headers):

    limit = headers.get("x-ratelimit-limit", "Unknown")
    remaining = headers.get("x-ratelimit-remaining", "Unknown")
    used = headers.get("x-ratelimit-used", "Unknown")
    reset = headers.get("x-ratelimit-reset", "Unknown")

    print("\n==============================")
    print("OpenAQ API Rate Limit Status")
    print("==============================")

    print(f"Timestamp          : {datetime.now()} UTC")
    print(f"Rate Limit         : {limit}")
    print(f"Requests Used      : {used}")
    print(f"Requests Remaining : {remaining}")
    print(f"Reset Timer (sec)  : {reset}")

    print("==============================\n")


def main():

    print("[INFO] Checking OpenAQ API status...")

    response = requests.get(
        BASE_URL,
        headers=HEADERS,
        timeout=30
    )

    print(f"[INFO] HTTP Status: {response.status_code}")

    if response.status_code == 401:
        print("[ERROR] Invalid API key.")
        return

    if response.status_code != 200:
        print("[ERROR] Unexpected response.")
        print(response.text)
        return

    print("[INFO] API key is valid.")

    print_rate_limit_info(response.headers)


if __name__ == "__main__":
    main()