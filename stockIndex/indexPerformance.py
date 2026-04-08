import pandas as pd
import numpy as np


def enforce_time_window(stock, index, days=365):

    stock = stock.copy()
    index = index.copy()

    end_date = min(stock.index.max(), index.index.max())
    start_date = end_date - pd.Timedelta(days=days)

    stock = stock.loc[start_date:end_date]
    index = index.loc[start_date:end_date]

    if len(stock) < 200 or len(index) < 200:
        raise ValueError("Insufficient data in 1Y window")

    return stock, index, start_date, end_date


def normalize_data(data, base_value):

    data = data.copy()
    close = data["Close"].dropna().sort_index()

    if len(close) == 0:
        raise ValueError("No valid Close data")

    data["normalized"] = (close / base_value) * 100

    return data


def align_data(stock, index):

    df = stock[["normalized"]].join(
        index[["normalized"]],
        how="inner",
        lsuffix="_stock",
        rsuffix="_index"
    ).dropna()

    if len(df) < 200:
        raise ValueError("Not enough overlapping trading days")

    return df


def compute_performance(stock_df, index_df):

    stock_df, index_df, start_date, end_date = enforce_time_window(stock_df, index_df)

    base_stock = stock_df["Close"].iloc[0]
    base_index = index_df["Close"].iloc[0]

    stock_df = normalize_data(stock_df, base_stock)
    index_df = normalize_data(index_df, base_index)

    df = align_data(stock_df, index_df)

    df['returns_stock'] = df['normalized_stock'].pct_change()
    df['returns_index'] = df['normalized_index'].pct_change()

    df['alpha_daily'] = df['returns_stock'] - df['returns_index']
    df['alpha_rolling'] = df['alpha_daily'].rolling(20, min_periods=5).mean()

    df["alpha_cumulative"] = df["normalized_stock"] - df["normalized_index"]

    df["relative_strength"] = df["normalized_stock"] / df["normalized_index"]
    df["rs_ma"] = df["relative_strength"].rolling(20, min_periods=5).mean()

    return df, start_date, end_date


def performance_summary(df, start_date, end_date):

    alpha_std = df["alpha_daily"].std()
    alpha_mean = df["alpha_daily"].mean()

    days = (end_date - start_date).days

    stock_drawdown = ((df["normalized_stock"] / df["normalized_stock"].cummax()) - 1) * 100

    summary = {

        "stock_return": df["normalized_stock"].iloc[-1] - 100,
        "index_return": df["normalized_index"].iloc[-1] - 100,
        "alpha": df["alpha_cumulative"].iloc[-1],

        "stock_cagr": ((df["normalized_stock"].iloc[-1] / 100) ** (365 / days)) - 1,
        "index_cagr": ((df["normalized_index"].iloc[-1] / 100) ** (365 / days)) - 1,

        "outperformance_days_pct": (df["alpha_daily"] > 0).mean() * 100,
        "underperformance_days_pct": (df["alpha_daily"] < 0).mean() * 100,

        "max_outperformance": df["alpha_cumulative"].max(),
        "max_underperformance": df["alpha_cumulative"].min(),

        "stock_volatility": df["returns_stock"].std() * np.sqrt(252),
        "index_volatility": df["returns_index"].std() * np.sqrt(252),

        "information_ratio": (
            (alpha_mean / alpha_std) * np.sqrt(252)
            if alpha_std and not pd.isna(alpha_std) else None
        ),

        "relative_strength_latest": df["relative_strength"].iloc[-1],
        "relative_strength_trend": (
            df["relative_strength"].iloc[-1] - df["relative_strength"].iloc[-20]
        ) if len(df) > 20 else None,

        "alpha_trend_20d": df["alpha_rolling"].iloc[-1],

        "max_drawdown_stock": stock_drawdown.min(),

        "start_date": start_date,
        "end_date": end_date,
        "actual_days": days
    }

    return summary


def index_performance_pipeline(stock_df, index_df):

    df, start_date, end_date = compute_performance(stock_df, index_df)
    summary = performance_summary(df, start_date, end_date)

    return {
        "timeseries": df,
        "summary": summary
    }