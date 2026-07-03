"""
plots/loader.py
"""

import json

import pandas as pd

from plots.config import *


def load_metrics():

    return pd.read_json(

        RESULTS_DIR /

        "detector_comparison.json"

    )


def load_statistics():

    return pd.read_json(

        RESULTS_DIR /

        "pairwise_statistics.json"

    )


def load_attack_report():

    with open(

        ATTACK_DIR /

        "attack_report.json"

    ) as f:

        return json.load(f)


def load_attack_manifest():

    with open(

        ATTACK_DIR /

        "attack_manifest.json"

    ) as f:

        return json.load(f)