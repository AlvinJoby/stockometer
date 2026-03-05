import pandas as pd
from retrieveData import colname


def price_change(data,symbol):
    data[colname(symbol,"priceChange")] = data[colname(symbol,"Close")].diff()

def dailyReturns(data,symbol):
    data[colname(symbol,"dailyReturns")] = data[colname(symbol,"Close")].pct_change()*100





