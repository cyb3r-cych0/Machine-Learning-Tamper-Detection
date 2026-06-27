"""
eda/plotting/continental.py

Continental-level visualizations.

Public API
----------
generate_continental_plots() from `summary_df` and `combined_df`.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from .utils import save_figure


# -------------------------------------------------------
# PUBLIC
# -------------------------------------------------------

def generate_continental_plots(
    summary_df,
    combined_df,
    output_dir
):

    plot_dir = Path(output_dir) / "plots"

    _dataset_size(summary_df, plot_dir)

    _mean_pm25(summary_df, plot_dir)

    _station_count(summary_df, plot_dir)

    _sensor_count(summary_df, plot_dir)

    _missing(summary_df, plot_dir)

    _coverage(summary_df, plot_dir)

    _country_boxplots(combined_df, plot_dir)

    _country_distribution(combined_df, plot_dir)


# --------------------------------------------------------
# DATASET SIZE
# --------------------------------------------------------
def _dataset_size(
    summary_df,
    output_dir
):

    fig, ax = plt.subplots(figsize=(12,6))

    plot = summary_df.sort_values("rows")

    ax.barh(

        plot["country"],

        plot["rows"]

    )

    ax.set_xlabel("Records")

    ax.set_title("Dataset Size by Country")

    save_figure(

        fig,

        output_dir,

        "dataset_size"

    )


# --------------------------------------------------------
# MEAN PM2.5
# --------------------------------------------------------
def _mean_pm25(
    summary_df,
    output_dir
):

    fig, ax = plt.subplots(figsize=(12,6))

    plot = summary_df.sort_values("mean")

    ax.barh(

        plot["country"],

        plot["mean"]

    )

    ax.set_xlabel(

        "Mean PM$_{2.5}$"

    )

    ax.set_title(

        "Mean PM$_{2.5}$ Concentration"

    )

    save_figure(

        fig,

        output_dir,

        "mean_pm25"

    )


# --------------------------------------------------------
# STATION COUNT
# --------------------------------------------------------
def _station_count(
    summary_df,
    output_dir
):

    fig, ax = plt.subplots(figsize=(12,6))

    plot = summary_df.sort_values("stations")

    ax.barh(

        plot["country"],

        plot["stations"]

    )

    ax.set_xlabel("Monitoring Stations")

    ax.set_title("Monitoring Network")

    save_figure(

        fig,

        output_dir,

        "station_count"

    )


# --------------------------------------------------------
# SENSOR COUNT
# --------------------------------------------------------
def _sensor_count(
    summary_df,
    output_dir
):

    fig, ax = plt.subplots(figsize=(12,6))

    plot = summary_df.sort_values("sensors")

    ax.barh(

        plot["country"],

        plot["sensors"]

    )

    ax.set_xlabel("Sensors")

    ax.set_title("Sensors by Country")

    save_figure(

        fig,

        output_dir,

        "sensor_count"

    )


# --------------------------------------------------------
# MISSING DATA
# --------------------------------------------------------
def _missing(
    summary_df,
    output_dir
):

    fig, ax = plt.subplots(figsize=(12,6))

    plot = summary_df.sort_values(

        "missing_percent"

    )

    ax.barh(

        plot["country"],

        plot["missing_percent"]

    )

    ax.set_xlabel(

        "Missing (%)"

    )

    ax.set_title(

        "Missing Data Percentage"

    )

    save_figure(

        fig,

        output_dir,

        "missing"

    )


# --------------------------------------------------------
# OBSERVATION COVERAGE
# --------------------------------------------------------
def _coverage(
    summary_df,
    output_dir
):

    fig, ax = plt.subplots(

        figsize=(14,7)

    )

    plot = summary_df.sort_values(

        "start"

    ).reset_index(

        drop=True

    )

    for i, row in plot.iterrows():

        ax.hlines(

            y=i,

            xmin=row["start"],

            xmax=row["end"],

            linewidth=5

        )

    ax.set_yticks(

        range(len(plot))

    )

    ax.set_yticklabels(

        plot["country"]

    )

    ax.set_title(

        "Observation Period"

    )

    save_figure(

        fig,

        output_dir,

        "coverage"

    )


# --------------------------------------------------------
# COUNTRY BOXPLOTS
# --------------------------------------------------------
def _country_boxplots(
    combined_df,
    output_dir
):

    fig, ax = plt.subplots(

        figsize=(16,7)

    )

    combined_df.boxplot(

        column="value",

        by="country",

        rot=45,

        ax=ax

    )

    plt.suptitle("")

    ax.set_title(

        "PM$_{2.5}$ Distribution"

    )

    ax.set_ylabel(

        "PM$_{2.5}$"

    )

    save_figure(

        fig,

        output_dir,

        "country_boxplots"

    )


# --------------------------------------------------------
# DISTRIBUTION COMPARISON
# --------------------------------------------------------
def _country_distribution(
    combined_df,
    output_dir
):

    fig, ax = plt.subplots(

        figsize=(15,7)

    )

    for country in sorted(

        combined_df["country"].unique()

    ):

        values = combined_df.loc[

            combined_df["country"] == country,

            "value"

        ]

        values.plot(

            kind="density",

            ax=ax,

            linewidth=2,

            label=country

        )

    ax.set_xlabel(

        "PM$_{2.5}$"

    )

    ax.set_title(

        "Country Distribution Comparison"

    )

    ax.legend(

        fontsize=8,

        ncol=2

    )

    save_figure(

        fig,

        output_dir,

        "country_distribution"

    )