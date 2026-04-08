import yfinance as yf
import pandas as pd


def retrieve_data(symbol):
    try:
        data = yf.download(symbol, period="5y", interval="1d")

        if data is None or data.empty:
            raise ValueError(f"No data fetched for symbol: {symbol}")

        # Flatten MultiIndex columns
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = ['_'.join(col) for col in data.columns]

        print(data.tail())

        # Normalize to plain column names FIRST
        data = normalize_columns(data, symbol)

        # Drop rows where all OHLC fields are NaN (yfinance trailing empty row bug)
        ohlc_cols = [c for c in ["Open", "High", "Low", "Close"] if c in data.columns]
        if ohlc_cols:
            data = data.dropna(subset=ohlc_cols, how="all")

        if data.empty:
            raise ValueError(f"No valid data after cleaning for symbol: {symbol}")
        print(data.tail())
        return data

    except Exception as e:
        print(f"[ERROR] Data fetch failed for {symbol}: {e}")
        return pd.DataFrame()


def colname(symbol, col_name):
    return col_name + "_" + symbol


def retrieve_ltp(data):
    price_col = "Close"

    if data is None or data.empty:
        raise ValueError("Data is empty")

    if price_col not in data.columns:
        raise ValueError(f"{price_col} not found in data")

    if len(data) < 2:
        raise ValueError("Not enough data to calculate LTP change")

    price_series = data[price_col]

    tLTP = price_series.iloc[-1]
    yLTP = price_series.iloc[-2]

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
    return yf.Ticker(symbol)


def normalize_columns(data, symbol):
    rename_map = {}
    for col in ["Close", "Open", "High", "Low", "Volume"]:
        suffixed = f"{col}_{symbol}"
        if suffixed in data.columns:
            rename_map[suffixed] = col
    return data.rename(columns=rename_map)