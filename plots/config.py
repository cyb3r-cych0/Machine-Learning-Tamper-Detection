"""
plots/config.py
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESULTS_DIR = PROJECT_ROOT / "outputs" / "detection"

ATTACK_DIR = PROJECT_ROOT / "outputs" / "attacks"

PLOTS_DIR = PROJECT_ROOT / "plots" / "output"

LOG_DIR = PLOTS_DIR / "logs"

PLOTS_DIR.mkdir(

    parents=True,

    exist_ok=True

)

LOG_DIR.mkdir(

    parents=True,

    exist_ok=True

)

DPI = 300

FIGSIZE = (10, 6)

EXPORT_PNG = True

EXPORT_PDF = True

EXPORT_SVG = True

FONT_SIZE = 12

TITLE_SIZE = 14
