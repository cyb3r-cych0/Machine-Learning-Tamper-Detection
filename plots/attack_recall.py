"""
plots/attack_recall.py
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from detection.models import isolation_forest
from plots.export import save_figure
from plots.config import RESULTS_DIR


def attack_recall_plot():

    rolling = pd.read_json(

        RESULTS_DIR / "rolling_z-score" /

        "attack_recall_rolling_zscore.json"

    )

    isolation = pd.read_json(

        RESULTS_DIR / "isolation_forest" /

        "attack_recall_isolation_forest.json"

    )

    lstm = pd.read_json(

        RESULTS_DIR / "lstm_autoencoder" /

        "attack_recall_lstm_autoencoder.json"

    )

    attack_order = [

        "Constant Bias",

        "Gradual Drift",

        "Random Stealth",

        "Spike Suppression"

    ]

    rolling = (

        rolling

        [

            rolling.attack_type != "None"

        ]

        .set_index(

            "attack_type"

        )

        .loc[attack_order]

    )

    isolation = (

        isolation

        [

            isolation.attack_type != "None"

        ]

        .set_index(

            "attack_type"

        )

        .loc[attack_order]

    )

    lstm = (

        lstm

        [

            lstm.attack_type != "None"

        ]

        .set_index(

            "attack_type"

        )

        .loc[attack_order]

    )

    x = np.arange(

        len(

            attack_order

        )

    )

    width = 0.25

    fig, ax = plt.subplots(

        figsize=(10,6)

    )

    ax.bar(

        x-width,

        isolation.recall.astype(float),

        width,

        label="Isolation Forest"

    )

    ax.bar(

        x,

        rolling.recall.astype(float),

        width,

        label="Rolling Z-Score"

    )

    ax.bar(

        x+width,

        lstm.recall.astype(float),

        width,

        label="LSTM Autoencoder"

    )

    ax.set_xticks(

        x

    )

    ax.set_xticklabels(

        attack_order,

        rotation=10

    )

    ax.set_ylabel(

        "Recall"

    )

    ax.set_ylim(

        0,

        1

    )

    ax.set_title(

        "Attack-wise Detection Recall"

    )

    ax.grid(

        axis="y",

        alpha=0.30

    )

    ax.legend()

    fig.tight_layout()

    save_figure(

        fig,

        "Figure_4_AttackRecall"

    )