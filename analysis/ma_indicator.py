import pandas as pd
from retrieveData import colname

def calculate_sma(data,symbol,period):
    data['sma_indicator'] = (data[colname(symbol,'Close')].rolling(window=period)).mean()
    return data

def calculate_ema(data,symbol,period):
    data['ema_indicator'] = (data[colname(symbol,'Close')].ewm(span=period,adjust=False)).mean()
    return data