#!/usr/bin/env python3
"""
explain_anomalies.py

Explainable Environmental Cybersecurity Analysis

Purpose:
    - Explain detected PM2.5 anomalies
    - Compare normal vs attacked behavior
    - Interpret suspicious temporal regions
    - Support explainable environmental cybersecurity

Outputs:
    - anomaly explanation tables
    - temporal explanation plots
    - attack-type summaries
    - feature deviation analysis
"""

import argparse
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# DIRECTORIES
# ============================================================

OUTPUT_DIR = Path("data/explanations")
PLOTS_DIR = Path("plots/explanations")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
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
# ANOMALY SUMMARY
# ============================================================

def anomaly_summary(df):

    print("\n==============================")
    print("ANOMALY SUMMARY")
    print("==============================")

    summary = (
        df["attack_label"]
        .value_counts()
    )

    print(summary)

    return summary


# ============================================================
# DETECTION PERFORMANCE SUMMARY
# ============================================================

def detection_summary(df):

    print("\n==============================")
    print("DETECTION SUMMARY")
    print("==============================")

    methods = [
        "zscore_anomaly",
        "iforest_anomaly",
        "reconstruction_anomaly"
    ]

    for method in methods:

        total = df[method].sum()

        print(f"{method}: {total} anomalies")


# ============================================================
# FEATURE DEVIATION ANALYSIS
# ============================================================

def feature_deviation_analysis(df):

    print("\n==============================")
    print("FEATURE DEVIATION ANALYSIS")
    print("==============================")

    grouped = (
        df.groupby("attack_label")["value"]
        .agg(["mean", "std", "min", "max"])
    )

    print(grouped)

    output_path = (
        OUTPUT_DIR /
        "feature_deviation_summary.csv"
    )

    grouped.to_csv(output_path)

    print(f"\n[INFO] Saved: {output_path}")


# ============================================================
# TEMPORAL EXPLANATION PLOT
# ============================================================

def temporal_explanation_plot(df):

    anomalies = df[
        df["reconstruction_anomaly"] == 1
    ]

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

    plt.title(
        "Explained Environmental Anomalies"
    )

    plt.xlabel("Timestamp")
    plt.ylabel("PM2.5")

    plt.legend()

    plt.tight_layout()

    output_path = (
        PLOTS_DIR /
        "explained_anomalies.png"
    )

    plt.savefig(output_path)

    plt.close()

    print(f"[INFO] Saved: {output_path}")


# ============================================================
# ATTACK REGION ANALYSIS
# ============================================================

def suspicious_region_analysis(df):

    print("\n==============================")
    print("SUSPICIOUS REGION ANALYSIS")
    print("==============================")

    suspicious = df[
        (
            (df["zscore_anomaly"] == 1) |
            (df["iforest_anomaly"] == 1) |
            (df["reconstruction_anomaly"] == 1)
        )
    ]

    suspicious = suspicious[
        [
            "timestamp_utc",
            "value",
            "attack_label",
            "zscore_anomaly",
            "iforest_anomaly",
            "reconstruction_anomaly"
        ]
    ]

    print(suspicious.head(20))

    output_path = (
        OUTPUT_DIR /
        "suspicious_regions.csv"
    )

    suspicious.to_csv(output_path, index=False)

    print(f"\n[INFO] Saved: {output_path}")


# ============================================================
# COMPARISON PLOT
# ============================================================

def normal_vs_attack_plot(df):

    normal = df[
        df["attack_label"] == "normal"
    ]

    attacked = df[
        df["attack_label"] != "normal"
    ]

    plt.figure(figsize=(14, 6))

    plt.plot(
        normal["timestamp_utc"],
        normal["value"],
        label="Normal"
    )

    plt.scatter(
        attacked["timestamp_utc"],
        attacked["value"],
        label="Attacked"
    )

    plt.title(
        "Normal vs Manipulated PM2.5 Behavior"
    )

    plt.xlabel("Timestamp")
    plt.ylabel("PM2.5")

    plt.legend()

    plt.tight_layout()

    output_path = (
        PLOTS_DIR /
        "normal_vs_attacked.png"
    )

    plt.savefig(output_path)

    plt.close()

    print(f"[INFO] Saved: {output_path}")


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description="Explainable Environmental Cybersecurity"
    )

    parser.add_argument(
        "--csv",
        required=True,
        help="Path to anomaly prediction dataset"
    )

    args = parser.parse_args()

    df = load_dataset(args.csv)

    anomaly_summary(df)

    detection_summary(df)

    feature_deviation_analysis(df)

    suspicious_region_analysis(df)

    print("\n[INFO] Generating explanation plots...")

    temporal_explanation_plot(df)

    normal_vs_attack_plot(df)

    print("\n[INFO] Explainability analysis completed.")


# ============================================================
# ENTRYPOINT
# ============================================================

if __name__ == "__main__":
    main()