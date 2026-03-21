import pandas as pd
from retrieveData import colname

def calculate_sma(data,symbol,period):
    data['sma_indicator'] = (data[colname(symbol,'Close')].rolling(window=period)).mean()
    return data