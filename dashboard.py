# dashboard.py

import streamlit as st
import pandas as pd
from polygon_data import get_polygon_data
from yield_curve import get_yield_curve_spread

st.set_page_config(page_title="📉 Collapse Monitoring Dashboard", layout="wide")

st.title("📉 Real-Time Collapse Monitoring Dashboard")

# ========================
# Section 1: Asset Charts
# ========================

st.header("📊 Macro Asset Performance: Bitcoin, Gold, S&P 500")

@st.cache_data(ttl=300)  # Refreshes every 5 minutes
def load_asset_data():
    btc = get_polygon_data("X:BTCUSD").rename(columns={"close": "Bitcoin"})
    gld = get_polygon_data("GLD").rename(columns={"close": "Gold (GLD)"})
    spy = get_polygon_data("SPY").rename(columns={"close": "S&P 500 (SPY)"})

    df = pd.concat([btc, gld, spy], axis=1).dropna()
    return df.pct_change().cumsum() * 100

try:
    df_assets = load_asset_data()
    st.line_chart(df_assets)
    st.caption("Data source: Polygon.io | Auto-refreshes every 5 minutes")
except Exception as e:
    st.error(f"❌ Failed to load asset data: {e}")

# ================================
# Section 2: Yield Curve Analysis
# ================================

st.header("📉 Yield Curve Spread: 10Y - 2Y")

@st.cache_data(ttl=86400)  # Refreshes once per day
def load_yield_data():
    return get_yield_curve_spread()

try:
    df_spread = load_yield_data()
    st.line_chart(df_spread)
    st.caption("Data source: FRED (via pandas_datareader)")
except Exception as e:
    st.error(f"❌ Failed to load yield curve data: {e}")
