"""
plots/workflow_diagram.py
"""

from graphviz import Digraph

from plots.config import PLOTS_DIR


def workflow_diagram():

    dot = Digraph(

        "Framework",

        format="png"

    )

    dot.attr(

        rankdir="TB",

        splines="ortho",

        nodesep="0.45",

        ranksep="0.60",

        bgcolor="white"

    )

    dot.attr(

        "node",

        shape="box",

        style="rounded,filled",

        fontname="Arial",

        fontsize="12",

        margin="0.15,0.08"

    )

    dot.node(

        "A",

        "OpenAQ Dataset"

    )

    dot.node(

        "B",

        "Preprocessing\n& Feature Engineering"

    )

    dot.node(

        "C",

        "Attack Generation\n(Constant Bias\nGradual Drift\nSpike Suppression\nRandom Stealth)"

    )

    dot.node(

        "D",

        "Detection\n\nRolling Z-Score\nIsolation Forest\nLSTM Autoencoder"

    )

    dot.node(

        "E",

        "Statistical Evaluation\n\nBootstrap CI\nMcNemar\nWilcoxon"

    )

    dot.node(

        "F",

        "Performance Visualization\n\nMetrics\nHeatmaps\nConfusion Matrix"

    )

    dot.edge("A","B")

    dot.edge("B","C")

    dot.edge("C","D")

    dot.edge("D","E")

    dot.edge("E","F")

    output = str(

        PLOTS_DIR /

        "Figure_10_Framework"

    )

    dot.render(

        output,

        cleanup=True

    )

    dot.format = "pdf"

    dot.render(

        output,

        cleanup=True

    )

    dot.format = "svg"

    dot.render(

        output,

        cleanup=True

    )