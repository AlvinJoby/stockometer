import yfinance as yf
import pandas as pd

def retrieve_data(symbol):

    try:
        data = yf.download(symbol,period="6mo",interval="1d")
        data.columns = ['_'.join(col) for col in data.columns]
        return data
    except Exception as e:
        return {"status":False,"error":e}
    
def colname(symbol,col_name):
    return col_name+"_"+symbol

def retrieve_ltp(data,symbol):
    tLTP = data[colname(symbol,'Close')].iloc[-1]
    yLTP = data[colname(symbol,'Close')].iloc[-2]
    percentChange = ((tLTP-yLTP)/yLTP)*100
    return {
        "tLTP":tLTP,
        "yLTP":yLTP,
        "percentChange": percentChange
    }

def retrieve_companyInfo(symbol):
    ticker = yf.Ticker(symbol)
    return ticker
