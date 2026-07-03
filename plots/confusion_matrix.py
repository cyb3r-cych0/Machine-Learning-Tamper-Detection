"""
plots/confusion_matrix.py
"""

import json

import matplotlib.pyplot as plt
import numpy as np

from plots.export import save_figure
from plots.config import RESULTS_DIR


FILES = {

    "Isolation Forest":

        RESULTS_DIR / "isolation_forest" /
        "metrics_isolation_forest.json",

    "Rolling Z-Score":

        RESULTS_DIR / "rolling_z-score" /
        "metrics_rolling_zscore.json",

    "LSTM Autoencoder":

        RESULTS_DIR / "lstm_autoencoder" /
        "metrics_lstm_autoencoder.json"

}


def confusion_matrix_plot():
    fig = plt.figure(

        figsize=(16, 5)

    )

    gs = fig.add_gridspec(

        1,

        4,

        width_ratios=[1, 1, 1, 0.06],

        wspace=0.45

    )

    ax1 = fig.add_subplot(gs[0])

    ax2 = fig.add_subplot(gs[1])

    ax3 = fig.add_subplot(gs[2])

    cax = fig.add_subplot(gs[3])

    axes = [

        ax1,

        ax2,

        ax3

    ]

    for ax, (detector, path) in zip(

        axes,

        FILES.items()

    ):

        with open(

            path,

            encoding="utf-8"

        ) as f:

            data = json.load(f)[0]

        matrix = np.array(

            [

                [

                    float(data["tn"]),

                    float(data["fp"])

                ],

                [

                    float(data["fn"]),

                    float(data["tp"])

                ]

            ]

        )

        matrix = (

            matrix /

            matrix.sum(axis=1, keepdims=True)

        )

        image = ax.imshow(

            matrix,

            vmin=0,

            vmax=1,

            interpolation="nearest",

            aspect="equal"

        )

        ax.set_xticks(

            [0,1]

        )

        ax.set_xticklabels(

            [

                "Pred Normal",

                "Pred Attack"

            ],

            fontsize=9

        )

        ax.set_yticks(

            [0,1]

        )

        ax.set_yticklabels(

            [

                "True Normal",

                "True Attack"

            ],

            fontsize=9

        )

        ax.set_title(

            detector,

            fontsize=12,

            fontweight="bold"

        )

        for i in range(2):

            for j in range(2):
                value = matrix[i, j]

                ax.text(

                    j,

                    i,

                    f"{value:.2f}",

                    ha="center",

                    va="center",

                    fontsize=11,

                    fontweight="bold",

                    color="white" if value < 0.50 else "black"

                )

    cbar = fig.colorbar(

        image,

        cax=cax

    )

    cbar.set_label(

        "Normalized Frequency",

        fontsize=11,

        fontweight="bold"

    )

    fig.suptitle(

        "Normalized Confusion Matrices",

        fontsize=16,

        fontweight="bold"

    )

    fig.tight_layout(

        rect=[0, 0, 0.96, 0.94]

    )

    save_figure(

        fig,

        "Figure_7_ConfusionMatrices"

    )