"""
Post-run verification of EDA outputs.
"""

from pathlib import Path


EXPECTED_COUNTRY_FILES = [
    "summary.csv",
    "metadata.json",
]

EXPECTED_PLOTS = [
    "time_series.png",
    "rolling_statistics.png",
    "distribution.png",
    "seasonality.png",
    "station_comparison.png",
    "sensor_availability.png",
    "outliers.png",
    "publication_summary.png",
]


def verify_country_outputs(country_dir):

    missing = []

    for file in EXPECTED_COUNTRY_FILES:

        if not (country_dir / file).exists():

            missing.append(file)

    plot_dir = country_dir / "plots"

    for file in EXPECTED_PLOTS:

        if not (plot_dir / file).exists():

            missing.append(file)

    return missing