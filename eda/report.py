from pathlib import Path
import pandas as pd


def save_summary(report, stats, output_dir):

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    df = pd.DataFrame([

        {**report, **stats}

    ])

    df.to_csv(

        output_dir / "summary.csv",

        index=False

    )