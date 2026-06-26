from pathlib import Path

from .loader import load_dataset
from .validator import validate
from .features import engineer_features
from .statistics import summary
from .report import save_summary


def process_country(csv_file, output_root):

    df = load_dataset(csv_file)

    report = validate(df)

    df, country_ts = engineer_features(df)

    stats = summary(country_ts)

    country = report["country"]

    save_summary(

        report,

        stats,

        output_root / country

    )

    return df.copy(), report, stats