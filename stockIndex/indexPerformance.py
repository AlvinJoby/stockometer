import pandas as pd

from retrieveData import retrieve_data,normalize_columns
from analysis.daily_returns import daily_change

def normalize_data(data):
    close = data["Close"].dropna()
    base = close.iloc[0]

    data.loc[close.index, "normalized"] = (close / base) * 100

    return data

def align_data(stock, index):
    return stock[["normalized"]].join(
        index[["normalized"]],
        how="inner",
        lsuffix="_stock",
        rsuffix="_index"
    ).dropna()

def indexPerformance(index,stock_df):

    index_df = retrieve_data(index)
    index_df = normalize_columns(index_df,index)
    
    index_df = normalize_data(index_df)
    stock_df = normalize_data(stock_df)

    normalized_df = align_data(stock_df,index_df)
    

    



    


