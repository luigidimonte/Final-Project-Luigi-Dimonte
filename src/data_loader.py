"""
Data loading and downloading utilities for the Financial Crises Project.
"""

import os
import pandas as pd
import yfinance as yf

# Mapping of index names to Yahoo Finance tickers
INDICES = {
    "SP500": "^GSPC",
    "NASDAQ": "^IXIC",
    "STOXX50": "^STOXX50E",
    "FTSE100": "^FTSE",
}

DATA_DIR = "data/raw"


def download_and_save_indices(start="1985-01-01", end="2025-01-01"):
    """
    Download all indices using Yahoo Finance and save them as CSV files.
    Only needed if you want to refresh data.
    """
    os.makedirs(DATA_DIR, exist_ok=True)

    for name, ticker in INDICES.items():
        print(f"Downloading {name} ({ticker})...")
        df = yf.download(ticker, start=start, end=end)
        out_path = f"{DATA_DIR}/{name}.csv"
        df.to_csv(out_path)
        print(f"Saved {name} to {out_path}")

def load_indices():
    """
    Load all index CSV files from data/raw into a dictionary of DataFrames.
    The dictionary has the form:
        {"SP500": df_sp500, "NASDAQ": df_nasdaq, ...}

    Each DataFrame will have its Close prices forced to numeric.
    """
    data = {}
    for name in INDICES.keys():
        path = f"{DATA_DIR}/{name}.csv"
        print(f"Loading {name} from {path}...")

        df = pd.read_csv(path, index_col=0)

        # Force datetime index
        df.index = pd.to_datetime(df.index, errors="coerce")
        df = df.sort_index()

        # Force numeric Close
        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

        # Save in dictionary
        data[name] = df

    return data
