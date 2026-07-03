"""
plots/logger.py
"""

import logging

from plots.config import LOG_DIR


def setup_logger():

    logger = logging.getLogger(

        "plots"

    )

    logger.setLevel(

        logging.INFO

    )

    logger.handlers.clear()

    formatter = logging.Formatter(

        "%(asctime)s | %(levelname)s | %(message)s"

    )

    file_handler = logging.FileHandler(

        LOG_DIR / "plots.log"

    )

    file_handler.setFormatter(

        formatter

    )

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(

        formatter

    )

    logger.addHandler(

        file_handler

    )

    logger.addHandler(

        console_handler

    )

    return logger