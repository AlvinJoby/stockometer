import pandas as pd
from retrieveData import colname

def calculate_sma(data,symbol,period):
    data['sma_indicator'] = (data[colname(symbol,'Close')].rolling(window=period)).mean()
    return data

def calculate_ema(data,symbol,period):
    data['ema_'+str(period)] = (data[colname(symbol,'Close')].ewm(span=period,adjust=False)).mean()
    return data

def custom_ema(data,period,column,cname):
    data[cname] = (data[column].ewm(span=period,adjust=False)).mean()
    return data