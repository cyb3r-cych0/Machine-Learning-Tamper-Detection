from pathlib import Path
import pandas as pd
import fastparquet

from eda.loader import discover_datasets
from eda.pipeline import process_country
from eda.config import *


def main():

    datasets = discover_datasets(INPUT_DIR)

    all_frames = []

    continental = []

    for csv in datasets:
        print(f"\nReading: {csv.name}")

        df, report, stats = process_country(
            csv,
            COUNTRY_REPORT_DIR
        )

        print(
            "Country column:",
            df["country"].unique()
        )

        all_frames.append(df.copy())

        continental.append({

            **report,

            **stats

        })

    pd.DataFrame(

        continental

    ).to_csv(

        CONTINENTAL_DIR / "country_summary.csv",

        index=False

    )

    for i, df in enumerate(all_frames):
        print(i, df["country"].iloc[0], len(df))

    combined_df = pd.concat(
        all_frames,
        ignore_index=True,
        copy=False
    )

    print("\nCombined Dataset")
    print("---------------------------")
    print("Rows:", len(combined_df))
    print("Countries:", combined_df["country"].nunique())
    print(combined_df["country"].value_counts())

    output_file = CONTINENTAL_DIR / "combined_dataset.csv"

    combined_df.to_csv(
        output_file,
        index=False
    )

    combined_df.to_parquet(
        CONTINENTAL_DIR / "combined_dataset.parquet",
        index=False
    )

    print("\nSaved to:")
    print(output_file.resolve())


if __name__ == "__main__":

    main()