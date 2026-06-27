"""
Configure Directories
"""

from pathlib import Path

INPUT_DIR = Path("data/preprocessed")

OUTPUT_DIR = Path("outputs")

COUNTRY_REPORT_DIR = OUTPUT_DIR / "country_reports"

CONTINENTAL_DIR = OUTPUT_DIR / "continental"

ROLLING_WINDOW = 24

ZSCORE_THRESHOLD = 3

MONTHLY_FREQ = "ME"

SAVE_PNG = True

SAVE_PDF = True