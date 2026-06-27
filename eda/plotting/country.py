"""
eda/plotting/country.py

Country-level publication plots.

Public API
----------
generate_country_plots()

Private helpers
---------------
_time_series()
_rolling_statistics()

(Additional plot functions will be added in Part 2 and Part 3.)
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .utils import save_figure


# --------------------------------------------------------
# PUBLIC API
# --------------------------------------------------------

def generate_country_plots(
    df,
    country_ts,
    monthly_ts,
    country,
    output_dir
):

    output_dir = Path(output_dir)

    _time_series(
        monthly_ts,
        country,
        output_dir
    )

    _rolling_statistics(
        monthly_ts,
        output_dir
    )

    _distribution(
        country_ts,
        output_dir
    )

    _seasonality(
        df,
        output_dir
    )

    _station_comparison(
        df,
        output_dir
    )

    _sensor_availability(
        df,
        output_dir
    )

    _outliers(
        country_ts,
        output_dir
    )

    _publication_summary(
        df,
        country_ts,
        monthly_ts,
        country,
        output_dir
    )

# --------------------------------------------------------
# TIME SERIES
# --------------------------------------------------------

def _time_series(
    monthly_ts,
    country,
    output_dir
):

    plot_df = (

        monthly_ts

        .dropna(
            subset=["monthly_mean"]
        )

        .copy()

    )

    fig, ax = plt.subplots(
        figsize=(14,6)
    )

    ax.plot(

        plot_df["timestamp_utc"],

        plot_df["monthly_mean_plot"],

        linewidth=2.5,

        marker="o",

        markersize=4,

        label="Monthly Mean"

    )

    # Trend

    x = np.arange(len(plot_df))

    trend = np.poly1d(

        np.polyfit(

            x,

            plot_df["monthly_mean_plot"],

            1

        )

    )

    ax.plot(

        plot_df["timestamp_utc"],

        trend(x),

        linestyle="--",

        linewidth=2.5,

        label="Trend"

    )

    ax.set_title(

        f"{country} PM$_{{2.5}}$ Long-Term Trend"

    )

    ax.set_ylabel(

        "PM$_{2.5}$ (µg/m³)"

    )

    ax.legend()

    save_figure(

        fig,

        output_dir,

        "time_series"

    )


# --------------------------------------------------------
# ROLLING STATISTICS
# --------------------------------------------------------

def _rolling_statistics(
    monthly_ts,
    output_dir
):

    plot_df = (

        monthly_ts

        .dropna(
            subset=["monthly_mean"]
        )

        .copy()

    )

    fig, ax = plt.subplots(
        figsize=(14,6)
    )

    ax.plot(

        plot_df["timestamp_utc"],

        plot_df["monthly_mean_plot"],

        linewidth=2.5,

        label="Monthly Mean"

    )

    ax.fill_between(

        plot_df["timestamp_utc"],

        plot_df["monthly_mean_plot"]

        -

        plot_df["monthly_std_plot"],

        plot_df["monthly_mean_plot"]

        +

        plot_df["monthly_std_plot"],

        alpha=0.25,

        label="±1 Std"

    )

    ax.set_ylabel(

        "PM$_{2.5}$ (µg/m³)"

    )

    ax.set_title(

        "Monthly Variability"

    )

    ax.legend()

    save_figure(

        fig,

        output_dir,

        "rolling_statistics"

    )


# --------------------------------------------------------
# DISTRIBUTION
# --------------------------------------------------------

def _distribution(
    country_ts,
    output_dir
):

    fig, ax = plt.subplots(
        figsize=(10,6)
    )

    values = country_ts["value"].dropna()

    values = values[
        values >= 0
    ]

    ax.hist(
        values,
        bins=40,
        density=True,
        alpha=0.75
    )

    ax.axvline(
        values.mean(),
        linestyle="--",
        linewidth=2,
        label=f"Mean = {values.mean():.2f}"
    )

    ax.axvline(
        values.median(),
        linestyle=":",
        linewidth=2,
        label=f"Median = {values.median():.2f}"
    )

    ax.axvline(
        values.quantile(.95),
        linestyle="-.",
        linewidth=2,
        label=f"95th = {values.quantile(.95):.2f}"
    )

    ax.set_xlabel(
        "PM$_{2.5}$ (µg/m³)"
    )

    ax.set_ylabel(
        "Density"
    )

    ax.set_title(
        "PM$_{2.5}$ Distribution"
    )

    ax.legend()

    save_figure(
        fig,
        output_dir,
        "distribution"
    )

# --------------------------------------------------------
# SEASONALITY
# --------------------------------------------------------
def _seasonality(
    df,
    output_dir
):

    stats = (

        df

        .groupby("hour")["value"]

        .agg(

            [

                "mean",

                "std"

            ]

        )

    )

    fig, ax = plt.subplots(
        figsize=(10,6)
    )

    ax.plot(

        stats.index,

        stats["mean"],

        marker="o",

        linewidth=2.5

    )

    ax.fill_between(

        stats.index,

        stats["mean"]

        -

        stats["std"],

        stats["mean"]

        +

        stats["std"],

        alpha=.25

    )

    ax.set_xlabel("Hour")

    ax.set_ylabel("PM$_{2.5}$")

    ax.set_title("Average Diurnal Pattern")

    save_figure(

        fig,

        output_dir,

        "seasonality"

    )

# --------------------------------------------------------
# COMPARISON
# --------------------------------------------------------
def _station_comparison(
    df,
    output_dir
):

    station = (

        df

        .groupby("location_name")["value"]

        .mean()

        .sort_values()

    )

    fig, ax = plt.subplots(
        figsize=(12,6)
    )

    station.plot(

        kind="barh",

        ax=ax

    )

    ax.set_xlabel(
        "Mean PM$_{2.5}$"
    )

    ax.set_title(
        "Average PM$_{2.5}$ by Monitoring Station"
    )

    save_figure(

        fig,

        output_dir,

        "station_comparison"

    )

# --------------------------------------------------------
# AVAILABILITY
# --------------------------------------------------------
def _sensor_availability(
    df,
    output_dir
):

    counts = (

        df

        .groupby("sensor_id")

        .size()

        .sort_values()

    )

    fig, ax = plt.subplots(
        figsize=(12,6)
    )

    counts.plot(

        kind="bar",

        ax=ax

    )

    ax.set_xlabel(
        "Sensor ID"
    )

    ax.set_ylabel(
        "Observations"
    )

    ax.set_title(
        "Observations per Sensor"
    )

    save_figure(

        fig,

        output_dir,

        "sensor_availability"

    )

# --------------------------------------------------------
# OUTLIERS
# --------------------------------------------------------
def _outliers(
    country_ts,
    output_dir
):

    top_events = (

        country_ts

        .sort_values(
            by="zscore",
            ascending=False
        )

        .head(20)

        .copy()

    )

    fig, ax = plt.subplots(
        figsize=(14,7)
    )

    ax.plot(

        country_ts["timestamp_utc"],

        country_ts["value"],

        linewidth=1,

        alpha=0.25,

        label="PM$_{2.5}$"

    )

    ax.scatter(

        top_events["timestamp_utc"],

        top_events["value"],

        s=120,

        zorder=5,

        label="Top 20"

    )

    for _, row in top_events.head(10).iterrows():

        ax.annotate(

            f"{row['value']:.1f}",

            (

                row["timestamp_utc"],

                row["value"]

            ),

            xytext=(5,5),

            textcoords="offset points",

            fontsize=8

        )

    ax.set_title(

        "Extreme PM$_{2.5}$ Events"

    )

    ax.set_ylabel(

        "PM$_{2.5}$ (µg/m³)"

    )

    ax.legend()

    save_figure(

        fig,

        output_dir,

        "outliers"

    )

# --------------------------------------------------------
# PUBLICATION SUMMARY
# --------------------------------------------------------
def _publication_summary(
    df,
    country_ts,
    monthly_ts,
    country,
    output_dir
):

    plot_df = (

        monthly_ts

        .dropna(
            subset=["monthly_mean"]
        )

        .copy()

    )

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(16,10)
    )

    # ------------------------------------
    # Time Series
    # ------------------------------------

    axes[0,0].plot(

        plot_df["timestamp_utc"],

        plot_df["monthly_mean_plot"],

        linewidth=2

    )

    x = np.arange(len(plot_df))

    trend = np.poly1d(

        np.polyfit(

            x,

            plot_df["monthly_mean_plot"],

            1

        )

    )

    axes[0,0].plot(

        plot_df["timestamp_utc"],

        trend(x),

        linestyle="--"

    )

    axes[0,0].set_title("(a) Long-Term Trend")

    # ------------------------------------
    # Rolling Statistics
    # ------------------------------------

    axes[0,1].plot(

        plot_df["timestamp_utc"],

        plot_df["monthly_mean_plot"],

        linewidth=2

    )

    axes[0,1].fill_between(

        plot_df["timestamp_utc"],

        plot_df["monthly_mean_plot"]

        -

        plot_df["monthly_std_plot"],

        plot_df["monthly_mean_plot"]

        +

        plot_df["monthly_std_plot"],

        alpha=0.25

    )

    axes[0,1].set_title("(b) Monthly Variability")

    # ------------------------------------
    # Seasonality
    # ------------------------------------

    stats = (

        df

        .groupby("hour")["value"]

        .agg(

            [

                "mean",

                "std"

            ]

        )

    )

    axes[1,0].plot(

        stats.index,

        stats["mean"]

    )

    axes[1,0].fill_between(

        stats.index,

        stats["mean"]

        -

        stats["std"],

        stats["mean"]

        +

        stats["std"],

        alpha=.25

    )

    axes[1,0].set_title("(c) Diurnal Pattern")

    # ------------------------------------
    # Distribution
    # ------------------------------------

    axes[1,1].hist(

        country_ts["value"],

        bins=40

    )

    axes[1,1].set_title("(d) Distribution")

    fig.suptitle(

        f"{country} PM$_{{2.5}}$ Dataset Characteristics",

        fontsize=18

    )

    fig.tight_layout()

    save_figure(

        fig,

        output_dir,

        "publication_summary"

    )