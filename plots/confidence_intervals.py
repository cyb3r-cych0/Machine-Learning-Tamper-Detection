"""
plots/confidence_intervals.py
"""

import matplotlib.pyplot as plt
import pandas as pd

from plots.export import save_figure
from plots.config import RESULTS_DIR


DETECTOR_CI = {

    "Isolation Forest":
        pd.read_json(
            RESULTS_DIR / "isolation_forest" /
            "confidence_intervals_isolation_forest.json"
        ),

    "Rolling Z-Score":
        pd.read_json(
            RESULTS_DIR / "rolling_z-score" /
            "confidence_intervals_rolling_zscore.json"
        ),

    "LSTM Autoencoder":
        pd.read_json(
            RESULTS_DIR / "lstm_autoencoder" /
            "confidence_intervals_lstm_autoencoder.json"
        )

}

METRICS = {

    "f1": "F1-Score",

    "recall": "Recall",

    "roc_auc": "ROC-AUC"

}


def confidence_interval_plot():

    fig, axes = plt.subplots(

        1,

        3,

        figsize=(15,5),

        sharey=False

    )

    for ax, (metric, title) in zip(

        axes,

        METRICS.items()

    ):

        names = []

        means = []

        lower = []

        upper = []

        for detector, df in DETECTOR_CI.items():

            row = (

                df

                [

                    df["metric"] == metric

                ]

                .iloc[0]

            )

            mean = float(

                row["mean"]

            )

            ci_lower = float(

                row["lower"]

            )

            ci_upper = float(

                row["upper"]

            )

            names.append(

                detector

            )

            means.append(

                mean

            )

            lower.append(

                mean - ci_lower

            )

            upper.append(

                ci_upper - mean

            )

        ax.errorbar(

            names,

            means,

            yerr=[

                lower,

                upper

            ],

            fmt="o",

            markersize=10,

            capsize=8,

            elinewidth=2.5,

            linewidth=2

        )

        if metric == "roc_auc":

            ax.axhline(

                0.5,

                linestyle="--",

                linewidth=1.5,

                alpha=0.60

            )

            ax.set_ylim(

                0.45,

                0.70

            )

        elif metric == "recall":

            ax.set_ylim(

                0,

                0.60

            )

        else:

            ax.set_ylim(

                0,

                0.08

            )

        for i, value in enumerate(

            means

        ):

            ax.text(

                i,

                value +

                (ax.get_ylim()[1]-ax.get_ylim()[0])*0.03,

                f"{value:.3f}",

                ha="center",

                fontsize=10,

                fontweight="bold"

            )

        ax.set_title(

            title,

            fontsize=13,

            fontweight="bold"

        )

        ax.grid(

            axis="y",

            linestyle=":",

            alpha=0.25

        )

    fig.suptitle(

        "Bootstrap 95% Confidence Intervals Across Detectors",

        fontsize=16,

        fontweight="bold"

    )

    fig.tight_layout(

        rect=[0,0,1,0.95]

    )

    save_figure(

        fig,

        "Figure_6_ConfidenceIntervals"

    )