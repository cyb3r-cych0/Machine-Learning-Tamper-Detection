"""
Engineer Features
"""

import numpy as np


def engineer_features(df, window=24):

    df = df.copy()

    df["hour"] = df.timestamp_utc.dt.hour
    df["dayofweek"] = df.timestamp_utc.dt.dayofweek
    df["month"] = df.timestamp_utc.dt.month
    df["year"] = df.timestamp_utc.dt.year

    country_ts = (

        df

        .groupby("timestamp_utc")["value"]

        .mean()

        .reset_index()

        .sort_values("timestamp_utc")

    )

    country_ts["rolling_mean"] = (

        country_ts["value"]

        .rolling(window)

        .mean()

    )

    country_ts["rolling_std"] = (

        country_ts["value"]

        .rolling(window)

        .std()

    )

    mean = country_ts["value"].mean()

    std = country_ts["value"].std()

    country_ts["zscore"] = (

        country_ts["value"] - mean

    ) / std

    country_ts["outlier"] = (

        np.abs(country_ts["zscore"]) > 3

    )

    monthly_ts = (

        country_ts

        .set_index("timestamp_utc")

        .resample("ME")

        .agg(

            {

                "value": ["mean", "std"]

            }

        )

    )

    monthly_ts.columns = [

        "monthly_mean",

        "monthly_std"

    ]

    monthly_ts["monthly_mean_plot"] = (

        monthly_ts["monthly_mean"]

        .interpolate(

            method="linear",

            limit=3

        )

    )

    monthly_ts["monthly_std_plot"] = (

        monthly_ts["monthly_std"]

        .interpolate(

            method="linear",

            limit=3

        )

    )

    monthly_ts = (

        monthly_ts

        .reset_index()

    )

    return (

        df,

        country_ts,

        monthly_ts

    )