"""
Country and continental report generation.

This module ONLY writes reports.
No statistics are computed here.
"""

from pathlib import Path
import json
import pandas as pd


# -------------------------------------------------------
# Internal
# -------------------------------------------------------

def _prepare_directory(output_dir: Path):

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )


# -------------------------------------------------------
# Country Summary
# -------------------------------------------------------

def save_country_summary(
    report: dict,
    output_dir: Path
):

    _prepare_directory(output_dir)

    summary = pd.DataFrame(
        [report]
    )

    summary.to_csv(
        output_dir / "summary.csv",
        index=False
    )


# -------------------------------------------------------
# Country Metadata
# -------------------------------------------------------

def save_country_metadata(
    report: dict,
    output_dir: Path
):

    _prepare_directory(output_dir)

    metadata = {
        "country": report["country"],
        "dataset": {
            "rows": report["rows"],
            "columns": report["columns"],
            "duplicates": report["duplicates"],
            "missing_values": report["missing"],
            "missing_percent": report["missing_percent"]
        },

        "monitoring_network": {
            "stations": report["stations"],
            "sensors": report["sensors"]
        },

        "temporal_coverage": {
            "start": str(report["start"]),
            "end": str(report["end"]),
            "duration_days": report["duration_days"]
        },

        "statistics": {
            "mean": report["mean"],
            "median": report["median"],
            "std": report["std"],
            "variance": report["variance"],
            "minimum": report["minimum"],
            "maximum": report["maximum"],
            "range": report["range"],
            "q1": report["q1"],
            "q3": report["q3"],
            "iqr": report["iqr"],
            "p90": report["p90"],
            "p95": report["p95"],
            "p99": report["p99"],
            "skewness": report["skewness"],
            "kurtosis": report["kurtosis"]
        },

        "outliers": {
            "zscore": report["zscore_outliers"],
            "iqr": report["iqr_outliers"]
        }
    }

    with open(
        output_dir / "metadata.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            metadata,
            f,
            indent=4,
            ensure_ascii=False
        )

# -------------------------------------------------------
# Continental Summary
# -------------------------------------------------------

def save_continental_summary(
    summary_df: pd.DataFrame,
    output_dir: Path
):

    _prepare_directory(output_dir)

    summary_df.to_csv(
        output_dir / "country_summary.csv",
        index=False
    )


# -------------------------------------------------------
# Combined Dataset
# -------------------------------------------------------

def save_combined_dataset(
    combined_df: pd.DataFrame,
    output_dir: Path
):

    _prepare_directory(output_dir)

    combined_df.to_csv(
        output_dir / "combined_dataset.csv",
        index=False
    )

    combined_df.to_parquet(
        output_dir / "combined_dataset.parquet",
        index=False
    )


# -------------------------------------------------------
# Complete Continental Export
# -------------------------------------------------------

def save_continental_outputs(
    summary_df: pd.DataFrame,
    combined_df: pd.DataFrame,
    output_dir: Path
):

    save_continental_summary(
        summary_df,
        output_dir
    )

    save_combined_dataset(
        combined_df,
        output_dir
    )