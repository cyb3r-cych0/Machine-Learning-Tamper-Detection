"""
plots/significance.py
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from plots.export import save_figure
from plots.config import RESULTS_DIR


def significance_plot():

    df = pd.read_json(

        RESULTS_DIR /

        "pairwise_statistics.json"

    )

    detectors = sorted(

        set(df["detector_a"])

        |

        set(df["detector_b"])

    )

    detector_index = {

        detector: i

        for i, detector

        in enumerate(detectors)

    }

    matrices = {

        "McNemar p-value":

            np.ones(

                (3,3)

            ),

        "Wilcoxon p-value":

            np.ones(

                (3,3)

            )

    }

    for _, row in df.iterrows():

        i = detector_index[

            row["detector_a"]

        ]

        j = detector_index[

            row["detector_b"]

        ]

        matrices["McNemar p-value"][i,j] = row["mcnemar_p"]

        matrices["McNemar p-value"][j,i] = row["mcnemar_p"]

        matrices["Wilcoxon p-value"][i,j] = row["wilcoxon_p"]

        matrices["Wilcoxon p-value"][j,i] = row["wilcoxon_p"]

    fig = plt.figure(

        figsize=(14,5)

    )

    gs = fig.add_gridspec(

        1,

        3,

        width_ratios=[1, 1, 0.05],

        wspace=0.55

    )

    ax1 = fig.add_subplot(gs[0])

    ax2 = fig.add_subplot(gs[1])

    cax = fig.add_subplot(gs[2])

    images = []

    for ax, (title, matrix) in zip(

        [ax1, ax2],

        matrices.items()

    ):

        image = ax.imshow(

            matrix,

            vmin=0,

            vmax=0.05,

            aspect="equal"

        )

        images.append(

            image

        )

        ax.set_xticks(

            range(3)

        )

        ax.set_yticks(

            range(3)

        )

        ax.set_xticklabels(

            detectors,

            rotation=25,

            ha="right",

            fontsize=10

        )

        ax.set_yticklabels(

            detectors,

            fontsize=10

        )

        ax.set_title(

            title,

            fontsize=13,

            fontweight="bold"

        )

        for i in range(3):

            for j in range(3):

                value = matrix[i,j]

                label = (

                    "<0.001"

                    if value < 0.001

                    else f"{value:.3f}"

                )

                ax.text(

                    j,

                    i,

                    label,

                    ha="center",

                    va="center",

                    fontsize=9,

                    fontweight="bold",

                    color="white"

                    if value < 0.025

                    else "black"

                )

    cbar = fig.colorbar(

        images[0],

        cax=cax

    )

    cbar.set_label(

        "p-value",

        fontsize=11,

        fontweight="bold"

    )

    fig.suptitle(

        "Pairwise Statistical Significance",

        fontsize=16,

        fontweight="bold"

    )

    fig.tight_layout(

        rect=[0,0,1,0.95]

    )

    save_figure(

        fig,

        "Figure_8_Significance"
    )