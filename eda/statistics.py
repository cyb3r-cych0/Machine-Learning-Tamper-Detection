"""
Centralized descriptive statistics for country-level EDA.

This module is the ONLY location responsible for computing
dataset statistics. No statistics should be calculated in
validator.py, report.py or manager.py.
"""


def calculate_statistics(df, country_ts):
    """
    Compute descriptive statistics for a single country's dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        Original dataset.

    country_ts : pandas.DataFrame
        Country-level aggregated time series.

    Returns
    -------
    dict
        Statistics consumed by report.py and manager.py.
    """

    values = country_ts["value"].dropna()

    q1 = values.quantile(0.25)
    q3 = values.quantile(0.75)

    iqr = q3 - q1

    report = {

        # ----------------------------------
        # Dataset Information
        # ----------------------------------

        "country": df["country"].iloc[0],
        "rows": len(df),
        "columns": len(df.columns),
        "missing": int(df.isna().sum().sum()),
        "duplicates": int(df.duplicated().sum()),

        # ----------------------------------
        # Monitoring Network
        # ----------------------------------

        "stations": int(df["location_id"].nunique()),
        "sensors": int(df["sensor_id"].nunique()),

        # ----------------------------------
        # Temporal Coverage
        # ----------------------------------

        "start": df["timestamp_utc"].min(),
        "end": df["timestamp_utc"].max(),
        "duration_days": (
            df["timestamp_utc"].max()
            -
            df["timestamp_utc"].min()
        ).days,

        # ----------------------------------
        # Descriptive Statistics
        # ----------------------------------

        "mean": float(values.mean()),
        "median": float(values.median()),
        "std": float(values.std()),
        "variance": float(values.var()),
        "minimum": float(values.min()),
        "maximum": float(values.max()),
        "range": float(values.max() - values.min()),

        # ----------------------------------
        # Quartiles
        # ----------------------------------

        "q1": float(q1),
        "q3": float(q3),
        "iqr": float(iqr),

        # ----------------------------------
        # Percentiles
        # ----------------------------------

        "p90": float(values.quantile(0.90)),
        "p95": float(values.quantile(0.95)),
        "p99": float(values.quantile(0.99)),

        # ----------------------------------
        # Distribution Shape
        # ----------------------------------

        "skewness": float(values.skew()),
        "kurtosis": float(values.kurt()),

        # ----------------------------------
        # Outliers
        # ----------------------------------

        "zscore_outliers": int(country_ts["outlier"].sum()),
        "iqr_outliers": int(
            (
                (values < (q1 - 1.5 * iqr))
                |
                (values > (q3 + 1.5 * iqr))
            ).sum()
        ),

        # ----------------------------------
        # Data Quality
        # ----------------------------------

        "negative_values": int((values < 0).sum()),
        "zero_values": int((values == 0).sum()),
        "nan_values": int(values.isna().sum()),

        # ----------------------------------
        # Completeness
        # ----------------------------------

        "missing_percent": float(
            (
                df.isna().sum().sum()
                /
                (len(df) * len(df.columns))
            )
            * 100
        )
    }

    return report