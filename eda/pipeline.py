"""
Country-level EDA pipeline.

Responsibilities:
    1. Load dataset
    2. Validate schema
    3. Engineer features
    4. Compute statistics
    5. Save reports
    6. Generate plots
    7. Return processed dataframe and report
"""

from pathlib import Path

from .loader import load_dataset
from .validator import validate_dataset
from .features import engineer_features
from .statistics import calculate_statistics
from .report import (
    save_country_summary,
    save_country_metadata,
)

from .plotting.country import generate_country_plots


def process_country(
    csv_file: Path,
    output_root: Path,
):
    """
    Executes the complete EDA workflow
    for a single country dataset.

    Parameters
    ----------
    csv_file : Path
        Input CSV

    output_root : Path
        outputs/country_reports/

    Returns
    -------
    df : pd.DataFrame
        Original dataframe with engineered features

    report : dict
        Country statistics used later by manager.py
    """

    # ---------------------------------------
    # Load
    # ---------------------------------------

    df = load_dataset(csv_file)

    # ---------------------------------------
    # Validation
    # ---------------------------------------

    validate_dataset(df)

    # ---------------------------------------
    # Feature Engineering
    # ---------------------------------------

    (
        df,
        country_ts,
        monthly_ts,
    ) = engineer_features(df)

    # ---------------------------------------
    # Statistics
    # ---------------------------------------

    report = calculate_statistics(
        df=df,
        country_ts=country_ts,
    )

    country = report["country"]

    country_dir = (
        output_root /
        country
    )

    # ---------------------------------------
    # Reports
    # ---------------------------------------

    save_country_summary(
        report,
        country_dir
    )

    save_country_metadata(
        report,
        country_dir
    )

    # ---------------------------------------
    # Plots
    # ---------------------------------------

    generate_country_plots(

        df=df,

        country_ts=country_ts,

        monthly_ts=monthly_ts,

        country=country,

        output_dir=country_dir / "plots"

    )

    return (

        df.copy(),

        report

    )