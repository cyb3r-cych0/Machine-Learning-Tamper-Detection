"""
plots/campaign_summary.py
"""

import json
from collections import Counter

import matplotlib.pyplot as plt

from plots.export import save_figure
from plots.config import ATTACK_DIR


def campaign_summary_plot():

    with open(
        ATTACK_DIR / "attack_report.json",
        encoding="utf-8"
    ) as f:
        report = json.load(f)

    with open(
        ATTACK_DIR / "campaign.json",
        encoding="utf-8"
    ) as f:
        campaigns = json.load(f)

    # --------------------------------------------------
    # Summary statistics
    # --------------------------------------------------

    attack_counts = report["attack_types"]

    baseline = report["rows"]

    attacked = report["attacked_rows"]

    normal = baseline - attacked

    coverage = attacked / baseline * 100

    country_counts = Counter(

        campaign["country"]

        for campaign in campaigns

    )

    # --------------------------------------------------
    # Figure
    # --------------------------------------------------

    fig = plt.figure(

        figsize=(16,5)

    )

    gs = fig.add_gridspec(

        1,

        3,

        width_ratios=[1,1,1],

        wspace=0.40

    )

    ax1 = fig.add_subplot(gs[0])

    ax2 = fig.add_subplot(gs[1])

    ax3 = fig.add_subplot(gs[2])

    # ==================================================
    # Panel A
    # ==================================================

    attacks = list(

        attack_counts.keys()

    )

    counts = list(

        attack_counts.values()

    )

    bars = ax1.bar(

        attacks,

        counts

    )

    ax1.set_title(

        "Attack Type Distribution",

        fontsize=13,

        fontweight="bold"

    )

    ax1.set_ylabel(

        "Campaign Count"

    )

    ax1.tick_params(

        axis="x",

        rotation=18

    )

    ax1.grid(

        axis="y",

        linestyle=":",

        alpha=0.25

    )

    for bar in bars:

        ax1.text(

            bar.get_x() +

            bar.get_width()/2,

            bar.get_height()+0.2,

            f"{int(bar.get_height())}",

            ha="center",

            fontsize=10,

            fontweight="bold"

        )

    # ==================================================
    # Panel B
    # ==================================================

    wedges, _ = ax2.pie(

        [

            attacked,

            normal

        ],

        startangle=90,

        wedgeprops={

            "width":0.45

        }

    )

    ax2.text(

        0,

        0,

        f"{coverage:.2f}%\nCoverage",

        ha="center",

        va="center",

        fontsize=13,

        fontweight="bold"

    )

    ax2.legend(

        wedges,

        [

            "Attacked",

            "Normal"

        ],

        loc="lower center",

        bbox_to_anchor=(0.5,-0.12),

        frameon=False,

        ncol=2

    )

    ax2.set_title(

        "Attack Coverage",

        fontsize=13,

        fontweight="bold"

    )

    # ==================================================
    # Panel C
    # ==================================================

    countries = [

        country

        for country, _

        in sorted(

            country_counts.items(),

            key=lambda x: x[1],

            reverse=True

        )

    ]

    values = [

        value

        for _, value

        in sorted(

            country_counts.items(),

            key=lambda x: x[1],

            reverse=True

        )

    ]

    bars = ax3.barh(

        countries,

        values

    )

    ax3.invert_yaxis()

    ax3.set_xlabel(

        "Campaign Count"

    )

    ax3.set_title(

        "Campaign Distribution by Country",

        fontsize=13,

        fontweight="bold"

    )

    ax3.grid(

        axis="x",

        linestyle=":",

        alpha=0.25

    )

    for bar in bars:

        width = bar.get_width()

        ax3.text(

            width + 0.15,

            bar.get_y()

            + bar.get_height()/2,

            str(

                int(width)

            ),

            va="center",

            fontsize=10,

            fontweight="bold"

        )

    # ==================================================

    fig.suptitle(

        "Cyberattack Campaign Summary",

        fontsize=16,

        fontweight="bold"

    )

    fig.tight_layout(

        rect=[0,0,1,0.94]

    )

    save_figure(

        fig,

        "Figure_9_CampaignSummary"

    )