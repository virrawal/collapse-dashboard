# dashboard.py

import streamlit as st
import pandas as pd

from yield_curve import get_yield_curve_spread
from twelve_data import get_asset_data

st.set_page_config(page_title="Collapse Monitoring Dashboard", layout="wide")

st.title("Real-Time Collapse Monitoring Dashboard")

# ========================
# Section 1: Asset Charts
# ========================

st.header("Macro Asset Performance: Bitcoin, Gold, S&P 500")

@st.cache_data(ttl=300)  # Refreshes every 5 minutes
def load_asset_data():
    """
    Fetch historical price data for Bitcoin, Gold, and the S&P 500 ETF from Twelve Data,
    compute cumulative returns, and return a DataFrame of percentage returns.
    """
    # Fetch historical data for Bitcoin, Gold, and S&P 500 from Twelve Data
    btc = get_asset_data("BTC/USD").rename(columns={"BTC/USD": "Bitcoin"})
    gld = get_asset_data("GLD").rename(columns={"GLD": "Gold (GLD)"})
    spy = get_asset_data("SPY").rename(columns={"SPY": "S&P 500 (SPY)"})
    df = pd.concat([btc, gld, spy], axis=1).dropna()
    # Compute cumulative returns (percentage) from daily returns
    returns = df.pct_change().fillna(0)
    cumulative = (1 + returns).cumprod() - 1
    return cumulative * 100

try:
    df_assets = load_asset_data()
    st.line_chart(df_assets)
    st.caption("Data source: Twelve Data | Auto-refreshes every 5 minutes")
except Exception as e:
    st.error(f"❌ Failed to load asset data: {e}")

# ================================
# Section 2: Yield Curve Analysis
# ================================

st.header("Yield Curve Spread: 10Y - 2Y")

@st.cache_data(ttl=86400)  # Refreshes once per day
def load_yield_data():
    """
    Fetch the 10‑year minus 2‑year Treasury yield spread from the Federal Reserve (FRED) data.
    """
    return get_yield_curve_spread()

try:
    df_spread = load_yield_data()
    st.line_chart(df_spread)
    st.caption("Data source: FRED (via pandas_datareader)")
except Exception as e:
    st.error(f"❌ Failed to load yield curve data: {e}")

