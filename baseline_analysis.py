#!/usr/bin/env python3
"""
baseline_analysis.py -- behavioral based analysis

Behavioral Baseline Analysis
for the Environmental Cybersecurity project.

Purpose:
    - Learn normal PM2.5 behavior
    - Identify natural environmental dynamics
    - Establish anomaly baselines
    - Prepare for tampering simulation

Outputs:
    - Temporal continuity analysis
    - Outlier density analysis
    - Hourly consistency plots
    - Daily variance plots
    - Z-score anomaly candidates
    - Rolling behavior analysis
"""

import argparse
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# DIRECTORIES
# ============================================================

PLOTS_DIR = Path("plots/baseline")
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

def load_dataset(csv_path):

    print(f"[INFO] Loading dataset: {csv_path}")

    df = pd.read_csv(csv_path)

    df["timestamp_utc"] = pd.to_datetime(
        df["timestamp_utc"],
        utc=True,
        errors="coerce"
    )

    df = df.sort_values("timestamp_utc")

    return df


# ============================================================
# TEMPORAL GAP ANALYSIS
# ============================================================

def temporal_gap_analysis(df):

    print("\n==============================")
    print("TEMPORAL GAP ANALYSIS")
    print("==============================")

    df["time_diff"] = (
        df["timestamp_utc"]
        .diff()
        .dt.total_seconds() / 3600
    )

    gaps = df[df["time_diff"] > 2]

    print(f"Large Gaps (>2h): {len(gaps)}")

    if len(gaps) > 0:
        print(gaps[["timestamp_utc", "time_diff"]].head())


# ============================================================
# OUTLIER ANALYSIS
# ============================================================

def outlier_analysis(df):

    print("\n==============================")
    print("OUTLIER ANALYSIS")
    print("==============================")

    mean = df["value"].mean()
    std = df["value"].std()

    df["z_score"] = (
        (df["value"] - mean) / std
    )

    anomalies = df[df["z_score"].abs() > 3]

    print(f"Potential Outliers (|Z| > 3): {len(anomalies)}")

    return anomalies


# ============================================================
# HOURLY CONSISTENCY
# ============================================================

def plot_hourly_consistency(df):

    df["hour"] = df["timestamp_utc"].dt.hour

    hourly_avg = (
        df.groupby("hour")["value"]
        .mean()
    )

    plt.figure(figsize=(10, 6))

    plt.plot(
        hourly_avg.index,
        hourly_avg.values
    )

    plt.title("Hourly PM2.5 Behavioral Baseline")
    plt.xlabel("Hour of Day")
    plt.ylabel("Average PM2.5")

    plt.tight_layout()

    output_path = (
        PLOTS_DIR /
        "hourly_behavioral_baseline.png"
    )

    plt.savefig(output_path)

    plt.close()

    print(f"[INFO] Saved: {output_path}")


# ============================================================
# DAILY VARIANCE
# ============================================================

def plot_daily_variance(df):

    df["date"] = df["timestamp_utc"].dt.date

    daily_std = (
        df.groupby("date")["value"]
        .std()
    )

    plt.figure(figsize=(14, 6))

    plt.plot(
        daily_std.index,
        daily_std.values
    )

    plt.title("Daily PM2.5 Variance")
    plt.xlabel("Date")
    plt.ylabel("Standard Deviation")

    plt.tight_layout()

    output_path = (
        PLOTS_DIR /
        "daily_variance.png"
    )

    plt.savefig(output_path)

    plt.close()

    print(f"[INFO] Saved: {output_path}")


# ============================================================
# Z-SCORE ANOMALIES
# ============================================================

def plot_zscore_anomalies(df):

    anomalies = df[df["z_score"].abs() > 3]

    plt.figure(figsize=(14, 6))

    plt.plot(
        df["timestamp_utc"],
        df["value"],
        label="PM2.5"
    )

    plt.scatter(
        anomalies["timestamp_utc"],
        anomalies["value"]
    )

    plt.title("Potential PM2.5 Anomalies")
    plt.xlabel("Timestamp")
    plt.ylabel("PM2.5")

    plt.legend()

    plt.tight_layout()

    output_path = (
        PLOTS_DIR /
        "zscore_anomalies.png"
    )

    plt.savefig(output_path)

    plt.close()

    print(f"[INFO] Saved: {output_path}")


# ============================================================
# ROLLING BASELINE
# ============================================================

def plot_rolling_baseline(df):

    rolling_mean = (
        df["value"]
        .rolling(window=24)
        .mean()
    )

    rolling_std = (
        df["value"]
        .rolling(window=24)
        .std()
    )

    plt.figure(figsize=(14, 6))

    plt.plot(
        df["timestamp_utc"],
        rolling_mean,
        label="24H Rolling Mean"
    )

    plt.plot(
        df["timestamp_utc"],
        rolling_std,
        label="24H Rolling Std"
    )

    plt.title("Rolling Behavioral Baseline")
    plt.xlabel("Timestamp")
    plt.ylabel("PM2.5")

    plt.legend()

    plt.tight_layout()

    output_path = (
        PLOTS_DIR /
        "rolling_behavioral_baseline.png"
    )

    plt.savefig(output_path)

    plt.close()

    print(f"[INFO] Saved: {output_path}")


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description="Behavioral Baseline Analysis"
    )

    parser.add_argument(
        "--csv",
        required=True,
        help="Path to processed CSV dataset"
    )

    args = parser.parse_args()

    df = load_dataset(args.csv)

    temporal_gap_analysis(df)

    anomalies = outlier_analysis(df)

    print("\n[INFO] Generating baseline plots...")

    plot_hourly_consistency(df)

    plot_daily_variance(df)

    plot_zscore_anomalies(df)

    plot_rolling_baseline(df)

    print("\n[INFO] Baseline analysis completed.")


# ============================================================
# ENTRYPOINT
# ============================================================

if __name__ == "__main__":
    main()