import yfinance as yf
import pandas as pd

def retrieve_data(symbol):

    try:
        data = yf.download(symbol,period="1y")
        data.columns = ['_'.join(col) for col in data.columns]
        return data
    except Exception as e:
        return {"status":False,"error":e}
    
def colname(symbol,col_name):
    return col_name+"_"+symbol