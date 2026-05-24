#!/usr/bin/env python3
"""
robustness_testing.py

Robustness and Generalization Testing
for the Environmental Cybersecurity project.

Purpose:
    - Evaluate detector robustness under
      varying adversarial conditions
    - Test generalization across attack intensities
    - Measure resilience to environmental noise
    - Analyze detection stability

Robustness Scenarios:
    1. Increasing bias intensity
    2. Increasing drift magnitude
    3. Environmental noise injection
    4. Partial data loss
    5. Combined perturbations

Outputs:
    - robustness_summary.csv
    - robustness comparison plots
    - detector stability analysis
"""

import argparse
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score
)

# ============================================================
# DIRECTORIES
# ============================================================

OUTPUT_DIR = Path("data/robustness")
PLOTS_DIR = Path("plots/robustness")

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
# BASELINE LABELS
# ============================================================

def initialize_labels(df):

    df["is_attack"] = 0

    return df


# ============================================================
# BIAS ATTACK
# ============================================================

def apply_bias_attack(
        df,
        bias
):

    attacked = df.copy()

    start = int(len(df) * 0.3)
    end = int(len(df) * 0.5)

    attacked.loc[start:end, "value"] += bias

    attacked.loc[start:end, "is_attack"] = 1

    return attacked


# ============================================================
# DRIFT ATTACK
# ============================================================

def apply_drift_attack(
        df,
        drift_max
):

    attacked = df.copy()

    start = int(len(df) * 0.5)
    end = int(len(df) * 0.7)

    drift = np.linspace(
        0,
        drift_max,
        end - start + 1
    )

    attacked.loc[start:end, "value"] += drift

    attacked.loc[start:end, "is_attack"] = 1

    return attacked


# ============================================================
# NOISE INJECTION
# ============================================================

def inject_environmental_noise(
        df,
        noise_std
):

    noisy = df.copy()

    noise = np.random.normal(
        0,
        noise_std,
        len(df)
    )

    noisy["value"] += noise

    return noisy


# ============================================================
# PARTIAL DATA LOSS
# ============================================================

def simulate_data_loss(
        df,
        loss_fraction
):

    reduced = df.copy()

    remove_count = int(
        len(df) * loss_fraction
    )

    indices = np.random.choice(
        reduced.index,
        remove_count,
        replace=False
    )

    reduced = reduced.drop(indices)

    return reduced.sort_values(
        "timestamp_utc"
    )


# ============================================================
# Z-SCORE DETECTOR
# ============================================================

def zscore_detector(
        df,
        threshold=3
):

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

    zscore = (
        (df["value"] - rolling_mean)
        / rolling_std
    )

    predictions = (
        zscore.abs() > threshold
    ).astype(int)

    return predictions.fillna(0)


# ============================================================
# ISOLATION FOREST
# ============================================================

def iforest_detector(df):

    model = IsolationForest(
        contamination=0.10,
        random_state=42
    )

    preds = model.fit_predict(
        df[["value"]].fillna(0)
    )

    return (
        preds == -1
    ).astype(int)


# ============================================================
# RECONSTRUCTION ERROR
# ============================================================

def reconstruction_detector(
        df,
        threshold=20
):

    rolling_mean = (
        df["value"]
        .rolling(window=24)
        .mean()
    )

    error = (
        df["value"] - rolling_mean
    ).abs()

    preds = (
        error > threshold
    ).astype(int)

    return preds.fillna(0)


# ============================================================
# METRIC EVALUATION
# ============================================================

def evaluate_predictions(
        y_true,
        y_pred
):

    return {
        "precision":
            precision_score(
                y_true,
                y_pred,
                zero_division=0
            ),

        "recall":
            recall_score(
                y_true,
                y_pred,
                zero_division=0
            ),

        "f1_score":
            f1_score(
                y_true,
                y_pred,
                zero_division=0
            )
    }


# ============================================================
# ROBUSTNESS EXPERIMENT
# ============================================================

def robustness_experiment(df):

    results = []

    # --------------------------------------------------------
    # BIAS INTENSITY TESTS
    # --------------------------------------------------------

    bias_levels = [
        5,
        10,
        20,
        40
    ]

    for bias in bias_levels:

        attacked = apply_bias_attack(
            df,
            bias
        )

        evaluate_scenario(
            attacked,
            results,
            scenario=f"bias_{bias}"
        )

    # --------------------------------------------------------
    # DRIFT TESTS
    # --------------------------------------------------------

    drift_levels = [
        10,
        20,
        40,
        80
    ]

    for drift in drift_levels:

        attacked = apply_drift_attack(
            df,
            drift
        )

        evaluate_scenario(
            attacked,
            results,
            scenario=f"drift_{drift}"
        )

    # --------------------------------------------------------
    # NOISE TESTS
    # --------------------------------------------------------

    noise_levels = [
        2,
        5,
        10,
        20
    ]

    for noise in noise_levels:

        noisy = inject_environmental_noise(
            df,
            noise
        )

        attacked = apply_bias_attack(
            noisy,
            20
        )

        evaluate_scenario(
            attacked,
            results,
            scenario=f"noise_{noise}"
        )

    # --------------------------------------------------------
    # DATA LOSS TESTS
    # --------------------------------------------------------

    loss_levels = [
        0.05,
        0.10,
        0.20,
        0.30
    ]

    for loss in loss_levels:

        reduced = simulate_data_loss(
            df,
            loss
        )

        attacked = apply_bias_attack(
            reduced,
            20
        )

        evaluate_scenario(
            attacked,
            results,
            scenario=f"loss_{loss}"
        )

    return pd.DataFrame(results)


# ============================================================
# SCENARIO EVALUATION
# ============================================================

def evaluate_scenario(
        df,
        results,
        scenario
):

    y_true = df["is_attack"]

    methods = {
        "zscore":
            zscore_detector(df),

        "iforest":
            iforest_detector(df),

        "reconstruction":
            reconstruction_detector(df)
    }

    for method_name, preds in methods.items():

        metrics = evaluate_predictions(
            y_true,
            preds
        )

        results.append({
            "scenario": scenario,
            "method": method_name,
            "precision": metrics["precision"],
            "recall": metrics["recall"],
            "f1_score": metrics["f1_score"]
        })


# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(results_df):

    output_path = (
        OUTPUT_DIR /
        "robustness_summary.csv"
    )

    results_df.to_csv(
        output_path,
        index=False
    )

    print(f"[INFO] Saved: {output_path}")


# ============================================================
# ROBUSTNESS PLOT
# ============================================================

def robustness_plot(results_df):

    methods = results_df["method"].unique()

    for method in methods:

        subset = results_df[
            results_df["method"] == method
        ]

        plt.figure(figsize=(12, 6))

        plt.plot(
            subset["scenario"],
            subset["f1_score"],
            marker="o"
        )

        plt.xticks(rotation=45)

        plt.ylabel("F1-Score")

        plt.title(
            f"{method} Robustness Across Scenarios"
        )

        plt.tight_layout()

        output_path = (
            PLOTS_DIR /
            f"{method}_robustness.png"
        )

        plt.savefig(output_path)

        plt.close()

        print(f"[INFO] Saved: {output_path}")


# ============================================================
# PUBLICATION SUMMARY
# ============================================================

def publication_summary(results_df):

    print("\n==============================")
    print("ROBUSTNESS SUMMARY")
    print("==============================")

    grouped = (
        results_df.groupby("method")
        ["f1_score"]
        .mean()
    )

    print(grouped)

    best_method = grouped.idxmax()

    print(
        f"\nMost Robust Detector: "
        f"{best_method}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description="Robustness Testing"
    )

    parser.add_argument(
        "--csv",
        required=True,
        help="Path to processed dataset"
    )

    args = parser.parse_args()

    df = load_dataset(args.csv)

    df = initialize_labels(df)

    print(
        "[INFO] Running robustness experiments..."
    )

    results_df = robustness_experiment(df)

    save_results(results_df)

    print(
        "\n[INFO] Generating robustness plots..."
    )

    robustness_plot(results_df)

    publication_summary(results_df)

    print(
        "\n[INFO] Robustness testing completed."
    )


# ============================================================
# ENTRYPOINT
# ============================================================

if __name__ == "__main__":
    main()