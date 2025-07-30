# polygon_data.py

import os
import requests
import pandas as pd
from datetime import datetime, timedelta

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY", "_r72i_HrM8kxwAOdXFhpn9NWls4GfA5E")

def get_polygon_data(ticker: str, days_back: int = 180) -> pd.DataFrame:
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days_back)

    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}?adjusted=true&sort=asc&limit=5000&apiKey={POLYGON_API_KEY}"
    
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Polygon API error: {response.status_code} - {response.text}")
    
    data = response.json().get("results", [])
    if not data:
        raise ValueError("No data returned from Polygon")

    df = pd.DataFrame(data)
    df["t"] = pd.to_datetime(df["t"], unit="ms")
    df.set_index("t", inplace=True)
    df = df[["c"]]  # Close prices
    df.columns = [ticker]
    return df
