# twelve_data.py

"""
Helper functions for fetching macro asset price data using the Twelve Data API.

This module replaces the Polygon-based implementation to avoid paid plan requirements.
"""

import os
import pandas as pd
from twelvedata import TDClient
import streamlit as st


def get_asset_data(ticker: str, days_back: int = 180) -> pd.DataFrame:
    """
    Fetch historical daily closing prices for a given asset using the Twelve Data API.

    Parameters:
        ticker (str): The asset symbol (e.g., 'SPY', 'GLD', 'BTC/USD').
        days_back (int): Number of days of historical data to retrieve.

    Returns:
        pd.DataFrame: DataFrame with date index and a single column named after the ticker containing close prices.
    """
    # Retrieve Twelve Data API key from Streamlit secrets or environment variable
    api_key = st.secrets.get("TD_API_KEY", None) or os.getenv("TD_API_KEY")
    if not api_key:
        raise ValueError(
            "Twelve Data API key not found. Please add TD_API_KEY to Streamlit secrets or set the TD_API_KEY environment variable."
        )

    # Initialize Twelve Data client
    td = TDClient(apikey=api_key)

    # Request daily time series data; outputsize corresponds to number of data points
    data = td.time_series(symbol=ticker, interval="1day", outputsize=days_back).as_pandas()

    # Validate data
    if data.empty:
        raise ValueError(f"No data returned from Twelve Data for {ticker}")

    # Extract the close prices and rename column to the ticker symbol
    df = data[["close"]].rename(columns={"close": ticker})
    df.index = pd.to_datetime(df.index)

    return df
