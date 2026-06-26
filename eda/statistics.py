import pandas as pd


def summary(country_ts):

    return {

        "mean": country_ts.value.mean(),

        "median": country_ts.value.median(),

        "std": country_ts.value.std(),

        "min": country_ts.value.min(),

        "max": country_ts.value.max(),

        "outliers": int(country_ts.outlier.sum())

    }