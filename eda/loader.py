from pathlib import Path
import pandas as pd


def discover_datasets(input_dir):

    return sorted(Path(input_dir).glob("*.csv"))


def load_dataset(csv_file):

    df = pd.read_csv(
        csv_file,
        low_memory=False
    )

    df["timestamp_utc"] = pd.to_datetime(
        df["timestamp_utc"],
        utc=True
    )

    df.sort_values(
        "timestamp_utc",
        inplace=True
    )

    return df