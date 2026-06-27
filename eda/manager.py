"""
Top-level manager for the EDA package.
"""

import pandas as pd
import time

from .logger import setup_logger
from .verify import verify_country_outputs
from .config import (
    INPUT_DIR,
    COUNTRY_REPORT_DIR,
    CONTINENTAL_DIR,
)
from .loader import discover_datasets
from .pipeline import process_country
from .report import save_continental_outputs
from .plotting.continental import (
    generate_continental_plots,
)


def run():
    start = time.perf_counter()

    logger = setup_logger(CONTINENTAL_DIR)

    logger.info("EDA started")

    datasets = discover_datasets(INPUT_DIR)

    if len(datasets) == 0:
        raise FileNotFoundError(f"No CSV files found in {INPUT_DIR}")

    print(f"\nFound {len(datasets)} datasets\n")

    country_reports = []
    all_frames = []

    for csv_file in datasets:
        try:
            df, report = process_country(csv_file, COUNTRY_REPORT_DIR)

            missing = verify_country_outputs(COUNTRY_REPORT_DIR / report["country"])

            if missing:
                logger.warning(f"{report['country']} missing: {missing}")
            else:
                logger.info(f"{report['country']} completed")

            all_frames.append(df)
            country_reports.append(report)

        except Exception as e:
            logger.exception(f"{csv_file.name} failed")

            continue

        # df, report = process_country(
        #
        #     csv_file,
        #
        #     COUNTRY_REPORT_DIR
        #
        # )
        #
        # all_frames.append(df)
        #
        # country_reports.append(report)

    summary_df = pd.DataFrame(
        country_reports
    )

    combined_df = pd.concat(
        all_frames,
        ignore_index=True
    )

    save_continental_outputs(
        summary_df,
        combined_df,
        CONTINENTAL_DIR
    )

    generate_continental_plots(
        summary_df,
        combined_df,
        CONTINENTAL_DIR
    )

    elapsed = time.perf_counter() - start

    logger.info(f"EDA completed in {elapsed:.2f} seconds")
    logger.info(f"Countries processed: {len(country_reports)}")
    logger.info(f"Combined rows: {len(combined_df):,}")

    import json

    summary = {
        "countries_processed": len(country_reports),
        "combined_rows": int(len(combined_df)),
        "runtime_seconds": elapsed,
        "status": "SUCCESS"
    }

    with open(
            CONTINENTAL_DIR / "eda_execution_summary.json",
            "w",
            encoding="utf-8"
    ) as f:

        json.dump(
            summary,
            f,
            indent=4
        )

    print()
    print("=" * 60)
    print("EDA COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print()