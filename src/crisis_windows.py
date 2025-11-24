"""
Definition and labelling of crisis windows.
"""

from typing import Dict, List
import pandas as pd


# List of major crises to study (you can adjust the dates later if needed)
CRISES: List[dict] = [
    {
        "name": "dotcom_bubble",
        "start": "2000-03-01",
        "end": "2002-10-31",
    },
    {
        "name": "global_financial_crisis",
        "start": "2007-10-01",
        "end": "2009-03-31",
    },
    {
        "name": "european_debt_crisis",
        "start": "2011-07-01",
        "end": "2012-12-31",
    },
    {
        "name": "covid_crash",
        "start": "2020-02-15",
        "end": "2020-04-30",
    },
]


def label_crisis_periods(
    data: Dict[str, pd.DataFrame],
    pre_crisis_months: int = 6,
    post_crisis_months: int = 6,
) -> Dict[str, pd.DataFrame]:
    """
    Label each date as normal / pre_crisis / crisis / post_crisis.

    Parameters
    ----------
    data : dict
        Dictionary of DataFrames (same structure as returned by compute_features).
    pre_crisis_months : int
        Number of months before each crisis start to label as 'pre_crisis'.
    post_crisis_months : int
        Number of months after each crisis end to label as 'post_crisis'.

    Returns
    -------
    labelled_data : dict
        Dictionary with the same keys, where each DataFrame includes:
        - 'regime' column: 'normal', 'pre_crisis', 'crisis', 'post_crisis'
        - 'crisis_name' column: name of the crisis (or None)
        - 'is_crisis' (0/1)
        - 'is_pre_crisis' (0/1)
        - 'is_high_risk' (0/1)  # 1 if pre_crisis or crisis
    """

    labelled_data: Dict[str, pd.DataFrame] = {}

    # Convert crisis dates to Timestamp once
    crises_parsed = []
    for c in CRISES:
        crises_parsed.append(
            {
                "name": c["name"],
                "start": pd.to_datetime(c["start"]),
                "end": pd.to_datetime(c["end"]),
            }
        )

    for name, df in data.items():
        df = df.copy()

        # Initialise all periods as normal regime
        df["regime"] = "normal"
        df["crisis_name"] = None
        df["is_crisis"] = 0
        df["is_pre_crisis"] = 0
        df["is_high_risk"] = 0

        for crisis in crises_parsed:
            start = crisis["start"]
            end = crisis["end"]

            # Define pre- and post-crisis windows
            pre_start = start - pd.DateOffset(months=pre_crisis_months)
            post_end = end + pd.DateOffset(months=post_crisis_months)

            # Boolean masks
            crisis_mask = (df.index >= start) & (df.index <= end)
            pre_mask = (df.index >= pre_start) & (df.index < start)
            post_mask = (df.index > end) & (df.index <= post_end)

            # Apply labels
            df.loc[crisis_mask, "regime"] = "crisis"
            df.loc[crisis_mask, "crisis_name"] = crisis["name"]
            df.loc[crisis_mask, "is_crisis"] = 1

            df.loc[pre_mask, "regime"] = "pre_crisis"
            df.loc[pre_mask, "crisis_name"] = crisis["name"]
            df.loc[pre_mask, "is_pre_crisis"] = 1

            df.loc[post_mask, "regime"] = "post_crisis"
            df.loc[post_mask, "crisis_name"] = crisis["name"]

        # High risk = pre_crisis OR crisis
        df["is_high_risk"] = df["is_crisis"] | df["is_pre_crisis"]

        labelled_data[name] = df

        print(
            f"[OK] {name}: crisis labels assigned "
            f"(crisis days={df['is_crisis'].sum()}, "
            f"pre-crisis days={df['is_pre_crisis'].sum()})"
        )

    return labelled_data
