#!/usr/bin/env python3
"""
evaluate_framework.py

Research Evaluation Framework
for the Environmental Cybersecurity project.

Purpose:
    - Evaluate environmental anomaly detection methods
    - Compare cybersecurity detection performance
    - Analyze attack detectability
    - Generate publication-ready metrics and plots

Evaluation Focus:
    1. Precision
    2. Recall
    3. F1-Score
    4. False Positive Rate
    5. Attack Detectability
    6. Detection Method Comparison

Outputs:
    - evaluation_summary.csv
    - attack_detectability.csv
    - publication-quality plots
    - ranked detector performance
"""

import argparse
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    accuracy_score
)

# ============================================================
# DIRECTORIES
# ============================================================

OUTPUT_DIR = Path("data/evaluation")
PLOTS_DIR = Path("plots/evaluation")

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
# PREPARE GROUND TRUTH
# ============================================================

def prepare_ground_truth(df):

    df["is_attack"] = (
        df["attack_label"] != "normal"
    ).astype(int)

    return df


# ============================================================
# FALSE POSITIVE RATE
# ============================================================

def calculate_false_positive_rate(
        y_true,
        y_pred
):

    tn, fp, fn, tp = confusion_matrix(
        y_true,
        y_pred
    ).ravel()

    if (fp + tn) == 0:
        return 0

    return fp / (fp + tn)


# ============================================================
# METHOD EVALUATION
# ============================================================

def evaluate_method(
        df,
        method_column,
        method_name
):

    y_true = df["is_attack"]
    y_pred = df[method_column]

    precision = precision_score(
        y_true,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_true,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_true,
        y_pred,
        zero_division=0
    )

    accuracy = accuracy_score(
        y_true,
        y_pred
    )

    fpr = calculate_false_positive_rate(
        y_true,
        y_pred
    )

    return {
        "method": method_name,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "accuracy": accuracy,
        "false_positive_rate": fpr
    }


# ============================================================
# EVALUATE ALL METHODS
# ============================================================

def evaluate_all_methods(df):

    print("\n==============================")
    print("DETECTION METHOD EVALUATION")
    print("==============================")

    methods = [
        (
            "zscore_anomaly",
            "Rolling Z-Score"
        ),
        (
            "iforest_anomaly",
            "Isolation Forest"
        ),
        (
            "reconstruction_anomaly",
            "Reconstruction Error"
        )
    ]

    results = []

    for column, name in methods:

        metrics = evaluate_method(
            df,
            column,
            name
        )

        results.append(metrics)

        print(f"\n{name}")

        print(
            f"Precision          : "
            f"{metrics['precision']:.4f}"
        )

        print(
            f"Recall             : "
            f"{metrics['recall']:.4f}"
        )

        print(
            f"F1-Score           : "
            f"{metrics['f1_score']:.4f}"
        )

        print(
            f"Accuracy           : "
            f"{metrics['accuracy']:.4f}"
        )

        print(
            f"False Positive Rate: "
            f"{metrics['false_positive_rate']:.4f}"
        )

    results_df = pd.DataFrame(results)

    return results_df


# ============================================================
# SAVE EVALUATION SUMMARY
# ============================================================

def save_evaluation_summary(results_df):

    output_path = (
        OUTPUT_DIR /
        "evaluation_summary.csv"
    )

    results_df.to_csv(
        output_path,
        index=False
    )

    print(f"\n[INFO] Saved: {output_path}")


# ============================================================
# DETECTOR RANKING
# ============================================================

def detector_ranking(results_df):

    ranked = results_df.sort_values(
        by="f1_score",
        ascending=False
    )

    print("\n==============================")
    print("DETECTOR RANKING")
    print("==============================")

    print(
        ranked[
            [
                "method",
                "f1_score",
                "precision",
                "recall"
            ]
        ]
    )

    output_path = (
        OUTPUT_DIR /
        "detector_ranking.csv"
    )

    ranked.to_csv(
        output_path,
        index=False
    )

    print(f"\n[INFO] Saved: {output_path}")

    return ranked


# ============================================================
# ATTACK DETECTABILITY ANALYSIS
# ============================================================

def attack_detectability_analysis(df):

    print("\n==============================")
    print("ATTACK DETECTABILITY ANALYSIS")
    print("==============================")

    attack_types = [
        attack
        for attack in df["attack_label"].unique()
        if attack != "normal"
    ]

    results = []

    for attack in attack_types:

        attack_df = df[
            (
                (df["attack_label"] == attack) |
                (df["attack_label"] == "normal")
            )
        ]

        y_true = (
            attack_df["attack_label"] != "normal"
        ).astype(int)

        methods = {
            "Rolling Z-Score":
                "zscore_anomaly",

            "Isolation Forest":
                "iforest_anomaly",

            "Reconstruction Error":
                "reconstruction_anomaly"
        }

        for method_name, column in methods.items():

            y_pred = attack_df[column]

            recall = recall_score(
                y_true,
                y_pred,
                zero_division=0
            )

            results.append({
                "attack_type": attack,
                "method": method_name,
                "detectability_recall": recall
            })

    detectability_df = pd.DataFrame(results)

    print(detectability_df)

    output_path = (
        OUTPUT_DIR /
        "attack_detectability.csv"
    )

    detectability_df.to_csv(
        output_path,
        index=False
    )

    print(f"\n[INFO] Saved: {output_path}")

    return detectability_df


# ============================================================
# PERFORMANCE COMPARISON PLOT
# ============================================================

def performance_comparison_plot(results_df):

    metrics = [
        "precision",
        "recall",
        "f1_score"
    ]

    x = np.arange(len(results_df))

    width = 0.25

    plt.figure(figsize=(12, 6))

    for i, metric in enumerate(metrics):

        plt.bar(
            x + (i * width),
            results_df[metric],
            width=width,
            label=metric
        )

    plt.xticks(
        x + width,
        results_df["method"]
    )

    plt.ylabel("Score")

    plt.title(
        "Detection Method Performance Comparison"
    )

    plt.legend()

    plt.tight_layout()

    output_path = (
        PLOTS_DIR /
        "detector_performance_comparison.png"
    )

    plt.savefig(output_path)

    plt.close()

    print(f"[INFO] Saved: {output_path}")


# ============================================================
# FALSE POSITIVE COMPARISON
# ============================================================

def false_positive_plot(results_df):

    plt.figure(figsize=(10, 6))

    plt.bar(
        results_df["method"],
        results_df["false_positive_rate"]
    )

    plt.ylabel("False Positive Rate")

    plt.title(
        "False Positive Rate Comparison"
    )

    plt.tight_layout()

    output_path = (
        PLOTS_DIR /
        "false_positive_comparison.png"
    )

    plt.savefig(output_path)

    plt.close()

    print(f"[INFO] Saved: {output_path}")


# ============================================================
# ATTACK DETECTABILITY PLOT
# ============================================================

def attack_detectability_plot(df):

    pivot = df.pivot(
        index="attack_type",
        columns="method",
        values="detectability_recall"
    )

    pivot.plot(
        kind="bar",
        figsize=(12, 6)
    )

    plt.ylabel("Recall")

    plt.title(
        "Attack Detectability by Detection Method"
    )

    plt.tight_layout()

    output_path = (
        PLOTS_DIR /
        "attack_detectability.png"
    )

    plt.savefig(output_path)

    plt.close()

    print(f"[INFO] Saved: {output_path}")


# ============================================================
# PUBLICATION SUMMARY
# ============================================================

def publication_summary(results_df):

    best_method = results_df.sort_values(
        by="f1_score",
        ascending=False
    ).iloc[0]

    print("\n==============================")
    print("PUBLICATION SUMMARY")
    print("==============================")

    print(
        f"Best Performing Detector : "
        f"{best_method['method']}"
    )

    print(
        f"Best F1-Score            : "
        f"{best_method['f1_score']:.4f}"
    )

    print(
        f"Precision                : "
        f"{best_method['precision']:.4f}"
    )

    print(
        f"Recall                   : "
        f"{best_method['recall']:.4f}"
    )

    print(
        f"False Positive Rate      : "
        f"{best_method['false_positive_rate']:.4f}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description="Environmental Cybersecurity Evaluation"
    )

    parser.add_argument(
        "--csv",
        required=True,
        help="Path to anomaly prediction dataset"
    )

    args = parser.parse_args()

    df = load_dataset(args.csv)

    df = prepare_ground_truth(df)

    # ========================================================
    # METHOD EVALUATION
    # ========================================================

    results_df = evaluate_all_methods(df)

    save_evaluation_summary(results_df)

    ranked = detector_ranking(results_df)

    # ========================================================
    # ATTACK DETECTABILITY
    # ========================================================

    detectability_df = (
        attack_detectability_analysis(df)
    )

    # ========================================================
    # PLOTS
    # ========================================================

    print("\n[INFO] Generating evaluation plots...")

    performance_comparison_plot(results_df)

    false_positive_plot(results_df)

    attack_detectability_plot(detectability_df)

    # ========================================================
    # PUBLICATION SUMMARY
    # ========================================================

    publication_summary(results_df)

    print("\n[INFO] Evaluation completed.")


# ============================================================
# ENTRYPOINT
# ============================================================

if __name__ == "__main__":
    main()