# yield_curve.py

import pandas_datareader.data as web
from datetime import datetime, timedelta
import pandas as pd

def get_yield_curve_spread(days_back=180):
    end = datetime.today()
    start = end - timedelta(days=days_back)

    # 10-year and 2-year Treasury constant maturity rates
    df_10yr = web.DataReader('GS10', 'fred', start, end)
    df_2yr = web.DataReader('GS2', 'fred', start, end)

    df = pd.concat([df_10yr, df_2yr], axis=1)
    df.columns = ['10Y', '2Y']
    df['Spread (10Y - 2Y)'] = df['10Y'] - df['2Y']
    df = df.dropna()

    return df
