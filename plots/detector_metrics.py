"""
plots/detector_metrics.py
"""

import matplotlib.pyplot as plt

import pandas as pd

import numpy as np

from plots.loader import load_metrics

from plots.export import save_figure

from plots.config import *


METRICS = [

    "Accuracy",

    "Precision",

    "Recall",

    "F1",

    "ROC_AUC",

    "PR_AUC",

    "FPR"

]


def detector_metrics_plot():

    df = load_metrics()

    detectors = df["Detector"]

    x = np.arange(

        len(detectors)

    )

    width = 0.11

    fig, ax = plt.subplots(

        figsize=(14, 6)

    )

    for i, metric in enumerate(

        METRICS

    ):

        ax.bar(

            x + i * width,

            df[metric],

            width,

            label=metric

        )

    ax.set_xticks(

        x + width * 3

    )

    ax.set_xticklabels(

        detectors,

        rotation=10

    )

    ax.set_ylim(

        0,

        1

    )

    ax.set_ylabel(

        "Score"

    )

    ax.set_title(

        "Detector Performance Comparison"

    )

    ax.grid(

        axis="y",

        alpha=0.3

    )

    ax.legend(

        ncol=4,

        fontsize=9

    )

    fig.tight_layout()

    save_figure(

        fig,

        "Figure_3_DetectorComparison"

    )