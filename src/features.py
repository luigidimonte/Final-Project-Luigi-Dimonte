import numpy as np
import pandas as pd

def compute_features(data: dict) -> dict:
    """
    Compute log-returns, rolling volatility and drawdown for all indices.

    Parameters
    ----------
    data : dict
        Dictionary where each key = index name (e.g. 'SP500'),
        and each value = DataFrame with at least a 'Close' price column.

    Returns
    -------
    features : dict
        Dictionary with the same keys, each containing a DataFrame
        enriched with:
        - log_return
        - vol_30d
        - drawdown
    """

    features = {}

    for name, df in data.items():

        df = df.copy()

        # Ensure Close column is numeric
        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

        # Compute log returns
        df["log_return"] = np.log(df["Close"]).diff()

        # Rolling 30-day volatility
        df["vol_30d"] = df["log_return"].rolling(window=30).std()

        # Compute running max (peak)
        df["peak"] = df["Close"].cummax()

        # Drawdown = (price - peak) / peak
        df["drawdown"] = (df["Close"] - df["peak"]) / df["peak"]

        # Store result
        features[name] = df

        print(f"[OK] {name}: features computed "
              f"(null log_returns={df['log_return'].isna().sum()})")

    return features
