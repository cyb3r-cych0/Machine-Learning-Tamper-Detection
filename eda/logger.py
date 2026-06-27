"""
Centralized logging for the EDA package.
"""

import logging
from pathlib import Path


def setup_logger(log_dir: Path):

    log_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    logger = logging.getLogger("EDA")

    logger.setLevel(logging.INFO)

    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        log_dir / "eda.log",
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.addHandler(console_handler)

    return logger