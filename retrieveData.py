import yfinance as yf
import pandas as pd

import yfinance as yf
import pandas as pd

def retrieve_data(symbol):
    try:
        data = yf.download(symbol, period="1y", interval="1d")

        # Check empty immediately
        if data is None or data.empty:
            raise ValueError(f"No data fetched for symbol: {symbol}")

        # Flatten columns safely
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = ['_'.join(col) for col in data.columns]

        return data

    except Exception as e:
        print(f"[ERROR] Data fetch failed for {symbol}: {e}")
        return pd.DataFrame()  # always return DataFrame
    

def colname(symbol,col_name):
    return col_name+"_"+symbol

def retrieve_ltp(data, symbol):

    price_col = colname(symbol, 'Close')

    # 🔹 Validate data
    if data is None or data.empty:
        raise ValueError("Data is empty")

    if price_col not in data.columns:
        raise ValueError(f"{price_col} not found in data")

    if len(data) < 2:
        raise ValueError("Not enough data to calculate LTP change")

    price_series = data[price_col]

    tLTP = price_series.iloc[-1]
    yLTP = price_series.iloc[-2]

    # 🔹 Prevent division error
    if yLTP == 0:
        percentChange = 0
    else:
        percentChange = ((tLTP - yLTP) / yLTP) * 100

    return {
        "tLTP": tLTP,
        "yLTP": yLTP,
        "percentChange": percentChange
    }

def retrieve_companyInfo(symbol):
    ticker = yf.Ticker(symbol)
    print(ticker)
    return ticker
