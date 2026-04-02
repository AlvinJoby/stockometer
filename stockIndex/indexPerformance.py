import pandas as pd


def normalize_data(data):
    data = data.copy()
    close = data["Close"].dropna().sort_index()

    if len(close) == 0:
        raise ValueError("No valid Close data")

    base = close.iloc[0]
    data.loc[close.index, "normalized"] = (close / base) * 100

    return data


def align_data(stock, index):
    df = stock[["normalized"]].join(
        index[["normalized"]],
        how="inner",
        lsuffix="_stock",
        rsuffix="_index"
    ).dropna()

    if len(df) < 30:
        raise ValueError("Not enough overlapping data")

    return df


def compute_performance(stock_df, index_df):

    stock_df = normalize_data(stock_df)
    index_df = normalize_data(index_df)

    df = align_data(stock_df, index_df)

    df['returns_stock'] = df['normalized_stock'].pct_change()
    df['returns_index'] = df['normalized_index'].pct_change()

    df['alpha_daily'] = df['returns_stock'] - df['returns_index']
    df['alpha_rolling'] = df['alpha_daily'].rolling(20, min_periods=5).mean()
    df["alpha_cumulative"] = df["normalized_stock"] - df["normalized_index"]

    df["relative_strength"] = df["normalized_stock"] / df["normalized_index"]
    df["rs_ma"] = df["relative_strength"].rolling(20).mean()

    return df


def performance_summary(df):

    alpha_std = df["alpha_daily"].std()
    alpha_mean = df["alpha_daily"].mean()

    days = (df.index[-1] - df.index[0]).days

    summary = {
        "stock_return": df["normalized_stock"].iloc[-1] - 100,
        "index_return": df["normalized_index"].iloc[-1] - 100,
        "alpha": df["alpha_cumulative"].iloc[-1],

        "stock_cagr": ((df["normalized_stock"].iloc[-1] / 100) ** (365 / days)) - 1 if days > 0 else None,
        "index_cagr": ((df["normalized_index"].iloc[-1] / 100) ** (365 / days)) - 1 if days > 0 else None,

        "outperformance_days_pct": (df["alpha_daily"] > 0).mean() * 100,
        "underperformance_days_pct": (df["alpha_daily"] < 0).mean() * 100,

        "max_outperformance": df["alpha_cumulative"].max(),
        "max_underperformance": df["alpha_cumulative"].min(),

        "stock_volatility": df["returns_stock"].std() * (252 ** 0.5),
        "index_volatility": df["returns_index"].std() * (252 ** 0.5),

        "information_ratio": (
            (alpha_mean / alpha_std) * (252 ** 0.5)
            if alpha_std and not pd.isna(alpha_std) else None
        ),

        "relative_strength_latest": df["relative_strength"].iloc[-1],
        "relative_strength_trend": (
            df["relative_strength"].dropna().iloc[-1] -
            df["relative_strength"].dropna().iloc[-20]
        ) if len(df["relative_strength"].dropna()) > 20 else None,

        "alpha_trend_20d": df["alpha_rolling"].iloc[-1],

        "worst_alpha_drawdown": (
            df["alpha_cumulative"] - df["alpha_cumulative"].cummax()
        ).min()
    }

    return summary


def index_performance_pipeline(stock_df, index_df):

    df = compute_performance(stock_df, index_df)
    summary = performance_summary(df)

    return {
        "timeseries": df,
        "summary": summary
    }