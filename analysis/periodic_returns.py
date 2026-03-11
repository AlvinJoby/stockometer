import pandas as pd
from retrieveData import colname

def periodic_returns(data,symbol):
    adj_close =  data[colname(symbol,'Close')]
    periods = {
        "1D": 1,
        "1W": 5,
        "1M": 21,
        "6M": 126,
        "1Y": 252
    }
    returns = {}
    for label,period in periods.items():
        return_series = adj_close.pct_change(period)
        value = return_series.iloc[-1]
        returns[label] = value
    return returns
       