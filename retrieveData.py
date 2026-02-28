import yfinance as yf
import pandas as pd

def retrieve_data(symbol,start_date,end_date):

    try:
        data = yf.download(symbol,start=start_date,end=end_date)
        data.columns = ['_'.join(col) for col in data.columns]
        return data
    except Exception as e:
        return {"status":False,"error":e}
    
def colname(symbol,col_name):
    return col_name+"_"+symbol