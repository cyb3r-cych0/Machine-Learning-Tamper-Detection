#!/usr/bin/env python3
"""
simulate_attacks.py

Adversarial Tampering Simulation
for the Environmental Cybersecurity project.

Purpose:
    - Simulate realistic manipulation attacks
      against PM2.5 environmental sensor data
    - Generate attacked datasets
    - Preserve attack labels for evaluation
    - Support anomaly detection experiments

Attack Scenarios:
    1. Constant Bias Injection
    2. Gradual Drift Attack
    3. Spike Suppression
    4. Random Stealth Perturbation

Outputs:
    - attacked_dataset.csv
    - attack labels
    - comparison plots
"""

import argparse
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# DIRECTORIES
# ============================================================

OUTPUT_DIR = Path("data/attacked")
PLOTS_DIR = Path("plots/attacks")

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
# ATTACK 1 — CONSTANT BIAS
# ============================================================

def constant_bias_attack(
        df,
        bias=25,
        start_ratio=0.30,
        end_ratio=0.45
):

    attacked = df.copy()

    start = int(len(df) * start_ratio)
    end = int(len(df) * end_ratio)

    attacked.loc[start:end, "value"] += bias

    attacked.loc[start:end, "attack_label"] = (
        "constant_bias"
    )

    return attacked


# ============================================================
# ATTACK 2 — GRADUAL DRIFT
# ============================================================

def gradual_drift_attack(
        df,
        drift_max=40,
        start_ratio=0.50,
        end_ratio=0.70
):

    attacked = df.copy()

    start = int(len(df) * start_ratio)
    end = int(len(df) * end_ratio)

    drift_values = np.linspace(
        0,
        drift_max,
        end - start + 1
    )

    attacked.loc[start:end, "value"] += drift_values

    attacked.loc[start:end, "attack_label"] = (
        "gradual_drift"
    )

    return attacked


# ============================================================
# ATTACK 3 — SPIKE SUPPRESSION
# ============================================================

def spike_suppression_attack(
        df,
        threshold=150,
        suppression_factor=0.5
):

    attacked = df.copy()

    spikes = attacked["value"] > threshold

    attacked.loc[spikes, "value"] *= suppression_factor

    attacked.loc[spikes, "attack_label"] = (
        "spike_suppression"
    )

    return attacked


# ============================================================
# ATTACK 4 — RANDOM STEALTH NOISE
# ============================================================

def stealth_perturbation_attack(
        df,
        noise_std=5,
        fraction=0.10
):

    attacked = df.copy()

    sample_size = int(len(df) * fraction)

    indices = np.random.choice(
        attacked.index,
        size=sample_size,
        replace=False
    )

    noise = np.random.normal(
        0,
        noise_std,
        sample_size
    )

    attacked.loc[indices, "value"] += noise

    attacked.loc[indices, "attack_label"] = (
        "stealth_perturbation"
    )

    return attacked


# ============================================================
# INITIALIZE LABELS
# ============================================================

def initialize_labels(df):

    df["attack_label"] = "normal"

    return df


# ============================================================
# COMPARISON PLOT
# ============================================================

def plot_comparison(
        original_df,
        attacked_df
):

    plt.figure(figsize=(14, 6))

    plt.plot(
        original_df["timestamp_utc"],
        original_df["value"],
        label="Original"
    )

    plt.plot(
        attacked_df["timestamp_utc"],
        attacked_df["value"],
        label="Attacked"
    )

    plt.title(
        "Original vs Attacked PM2.5 Data"
    )

    plt.xlabel("Timestamp")
    plt.ylabel("PM2.5")

    plt.legend()

    plt.tight_layout()

    output_path = (
        PLOTS_DIR /
        "attack_comparison.png"
    )

    plt.savefig(output_path)

    plt.close()

    print(f"[INFO] Saved: {output_path}")


# ============================================================
# SAVE ATTACKED DATASET
# ============================================================

def save_dataset(df):

    output_path = (
        OUTPUT_DIR /
        "attacked_pm25_dataset.csv"
    )

    df.to_csv(output_path, index=False)

    print(f"[INFO] Saved: {output_path}")


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description="Environmental Sensor Attack Simulation"
    )

    parser.add_argument(
        "--csv",
        required=True,
        help="Path to processed CSV dataset"
    )

    args = parser.parse_args()

    df = load_dataset(args.csv)

    df = initialize_labels(df)

    original_df = df.copy()

    print("[INFO] Applying attacks...")

    df = constant_bias_attack(df)

    df = gradual_drift_attack(df)

    df = spike_suppression_attack(df)

    df = stealth_perturbation_attack(df)

    save_dataset(df)

    plot_comparison(
        original_df,
        df
    )

    print("\n[INFO] Attack simulation completed.")


# ============================================================
# ENTRYPOINT
# ============================================================

if __name__ == "__main__":
    main()