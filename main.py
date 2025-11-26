"""
Main entry point for the Financial Crises Project.

Pipeline:
1. Load data from data/raw
2. Compute basic features (log returns, volatility, drawdown)
3. (Later) Label crisis periods and run analysis
"""
import sys
import os

# Add project root so that "src" can be imported correctly
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_root)


from src.data_loader import load_indices, download_and_save_indices
from src.features import compute_features
from src.crisis_windows import label_crisis_periods
from src.analysis import run_analysis


def main(download: bool = False):
    """
    Run the full pipeline.

    Parameters
    ----------
    download : bool, optional
        If True, re-download all index data from Yahoo Finance and overwrite
        the CSV files in data/raw. By default False.
    """

    if download:
        print("Step 1: downloading data...")
        download_and_save_indices()
        print("Download completed.\n")

    print("Step 2: loading data from data/raw ...")
    raw_data = load_indices()
    print("Data loaded.\n")

    print("Step 3: computing features (returns, volatility, drawdown)...")
    data_with_features = compute_features(raw_data)
    print("Features computed.\n")
    print("Step 4: labeling crisis periods ...")
    labelled_data = label_crisis_periods(data_with_features)
    print("Crisis labels added. \n")
    print("Step 5: running analysis and saving results ...")
    run_analysis(labelled_data)
    print("Analysis completed.\n")



    # Placeholder for future steps
    # TODO: label crisis periods and run analysis

    print("Pipeline finished successfully.")

    return labelled_data


if __name__ == "__main__":
    # By default we do NOT re-download data, we just use existing CSVs.
    main(download=False)
