"""
plots/export.py
"""

from plots.config import *

import matplotlib.pyplot as plt


def save_figure(

    figure,

    filename

):

    if EXPORT_PNG:

        figure.savefig(

            PLOTS_DIR / f"{filename}.png",

            dpi=DPI,

            bbox_inches="tight"

        )

    if EXPORT_PDF:

        figure.savefig(

            PLOTS_DIR / f"{filename}.pdf",

            bbox_inches="tight"

        )

    if EXPORT_SVG:

        figure.savefig(

            PLOTS_DIR / f"{filename}.svg",

            bbox_inches="tight"

        )

    plt.close(

        figure

    )