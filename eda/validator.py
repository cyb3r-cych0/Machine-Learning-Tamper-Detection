"""
Validate Dataset Metrics
"""

def validate_dataset(df):

    report = {

        "rows": len(df),
        "missing": int(df.isna().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
        "stations": df["location_id"].nunique(),
        "sensors": df["sensor_id"].nunique(),
        "start": df["timestamp_utc"].min(),
        "end": df["timestamp_utc"].max(),
        "country": df["country"].iloc[0]
    }

    return report