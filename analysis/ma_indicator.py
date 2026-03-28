import pandas as pd

def calculate_sma(data,period):
    data['sma_indicator'] = (data['Close'].rolling(window=period)).mean()
    return data

def calculate_ema(data,period):
    data['ema_'+str(period)] = (data['Close'].ewm(span=period,adjust=False)).mean()
    return data

def custom_ema(data,period,column,cname):
    data[cname] = (data[column].ewm(span=period,adjust=False)).mean()
    return data