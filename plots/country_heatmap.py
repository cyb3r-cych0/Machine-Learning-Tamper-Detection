"""
plots/country_heatmap.py
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from plots.export import save_figure
from plots.config import RESULTS_DIR


def country_heatmap_plot():

    rolling = pd.read_json(

        RESULTS_DIR / "rolling_z-score" /

        "country_recall_rolling_zscore.json"

    )

    isolation = pd.read_json(

        RESULTS_DIR / "isolation_forest" /

        "country_recall_isolation_forest.json"

    )

    lstm = pd.read_json(

        RESULTS_DIR / "lstm_autoencoder" /

        "country_recall_lstm_autoencoder.json"

    )

    rolling = rolling.rename(

        columns={

            "recall":

            "Rolling Z-Score"

        }

    )

    isolation = isolation.rename(

        columns={

            "recall":

            "Isolation Forest"

        }

    )

    lstm = lstm.rename(

        columns={

            "recall":

            "LSTM Autoencoder"

        }

    )

    df = (

        rolling

        .merge(

            isolation,

            on="country"

        )

        .merge(

            lstm,

            on="country"

        )

    )

    countries = df["country"]

    matrix = (

        df

        .drop(

            columns="country"

        )

        .astype(float)

        .values

    )

    fig = plt.figure(

        figsize=(9, 8)

    )

    gs = fig.add_gridspec(

        1,

        2,

        width_ratios=[1, 0.06],

        wspace=0.12

    )

    ax = fig.add_subplot(gs[0])

    cax = fig.add_subplot(gs[1])

    image = ax.imshow(

        matrix,

        aspect="auto",

        interpolation="nearest",

        vmin=0,

        vmax=1.0

    )

    for i in range(matrix.shape[0]):

        for j in range(matrix.shape[1]):
            value = matrix[i, j]

            ax.text(

                j,

                i,

                f"{value:.2f}",

                ha="center",

                va="center",

                fontsize=8,

                color="white" if value < 0.35 else "black",

                fontweight="bold"

            )

    ax.set_xticks(

        np.arange(3)

    )

    ax.set_xticklabels(

        [

            "Rolling\nZ-Score",

            "Isolation\nForest",

            "LSTM\nAutoencoder"

        ]

    )

    ax.set_yticks(

        np.arange(

            len(countries)

        )

    )

    ax.set_yticklabels(

        countries

    )

    ax.set_xlabel(

        "Detector"

    )

    ax.set_ylabel(

        "Country"

    )

    ax.set_title(

        "Country-wise Detection Recall"

    )

    cbar = fig.colorbar(

        image,

        cax=cax

    )

    cbar.set_label(

        "Recall",

        fontsize=11,

        fontweight="bold"

    )

    cbar.set_label(

        "Recall"

    )

    fig.tight_layout()

    save_figure(

        fig,

        "Figure_5_CountryHeatmap"

    )