"""
Analysis utilities for the Financial Crises Project.

This module:
- computes summary statistics by regime (normal / pre_crisis / crisis / post_crisis)
- saves CSV tables to results/
- saves panel plots (price, volatility, drawdown) to results/
"""

import os
from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd


def _ensure_results_dir(out_dir: str) -> None:
    """Create the results directory if it does not exist."""
    os.makedirs(out_dir, exist_ok=True)


def regime_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute summary statistics by regime for a single index.

    Parameters
    ----------
    df : DataFrame
        Must contain columns:
        - 'regime'
        - 'log_return'
        - 'vol_30d'
        - 'drawdown'

    Returns
    -------
    summary : DataFrame
        Table with mean, std, min, max of each variable by regime.
    """
    summary = (
        df.groupby("regime")[["log_return", "vol_30d", "drawdown"]]
        .agg(["mean", "std", "min", "max"])
    )
    return summary


def plot_index_panels(df: pd.DataFrame, name: str, out_dir: str = "results") -> None:
    """
    Plot price, volatility and drawdown panels for a given index and save to file.
    """
    _ensure_results_dir(out_dir)

    fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

    # Price
    axes[0].plot(df.index, df["Close"])
    axes[0].set_title(f"{name} - Close price")
    axes[0].set_ylabel("Price")

    # Volatility (30-day rolling)
    axes[1].plot(df.index, df["vol_30d"])
    axes[1].set_title(f"{name} - 30-day rolling volatility")
    axes[1].set_ylabel("Volatility")

    # Drawdown
    axes[2].plot(df.index, df["drawdown"])
    axes[2].set_title(f"{name} - Drawdown")
    axes[2].set_ylabel("Drawdown")
    axes[2].set_xlabel("Date")

    fig.tight_layout()

    out_path = os.path.join(out_dir, f"{name}_panels.png")
    fig.savefig(out_path)
    plt.close(fig)

    print(f"[OK] Saved plot for {name} to {out_path}")


def run_analysis(labelled_data: Dict[str, pd.DataFrame], out_dir: str = "results") -> None:
    """
    Run the full analysis for all indices:
    - save regime summary tables as CSV
    - save panel plots (price, volatility, drawdown)

    Parameters
    ----------
    labelled_data : dict
        Output of label_crisis_periods (dict of DataFrames, one per index).
    out_dir : str
        Directory where results will be stored.
    """
    _ensure_results_dir(out_dir)

    all_summaries = []

    for name, df in labelled_data.items():
        # 1) Save summary statistics by regime for this index
        summary = regime_summary(df)
        summary_path = os.path.join(out_dir, f"{name}_regime_summary.csv")
        summary.to_csv(summary_path)
        print(f"[OK] Saved regime summary for {name} to {summary_path}")

        # Keep a flattened version for a global summary
        flat = summary.copy()
        flat["index"] = name
        all_summaries.append(flat)

        # 2) Save plots
        plot_index_panels(df, name, out_dir=out_dir)

    # Optional: global summary across indices
    if all_summaries:
        combined = pd.concat(all_summaries)
        combined_path = os.path.join(out_dir, "all_indices_regime_summary.csv")
        combined.to_csv(combined_path)
        print(f"[OK] Saved combined regime summary to {combined_path}")

    print("Analysis completed. All results saved in the 'results/' directory.")

