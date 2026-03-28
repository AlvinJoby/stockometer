from flask import Flask,render_template,request
from validation import validateInput
from retrieveData import retrieve_data,retrieve_ltp,retrieve_companyInfo,normalize_columns
from graph import generate_graph
from analysis.rsi_indicator import calculate_rsi,mark_signals
from analysis.ma_indicator import calculate_sma,calculate_ema
from analysis.periodic_returns import periodic_returns
from analysis.company_data import companyData,format_number
from analysis.daily_returns import price_change,dailyReturns
from analysis.macd_indicator import calculate_macd
from analysis.buysell_marker import marking_bs
import pandas as pd

import config


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/analyze',  methods=['POST'])
def analyze():
    symbol = request.form.get("symbol")
    validation_result = validateInput(symbol)
    

    if not validation_result["status"]:
        return validation_result["error"]
    
    data = retrieve_data(symbol)
    data = normalize_columns(data,symbol)
    

    config.symbol=symbol
    config.data=data

    LTP = retrieve_ltp(data)
    ticker = retrieve_companyInfo(symbol)
    company= companyData(ticker)

    company["marketCap"] = format_number(company["marketCap"])
    company["totalRevenue"] = format_number(company["totalRevenue"])
    company["netIncomeToCommon"] = format_number(company["netIncomeToCommon"])
    company["profitMargins"] = f"{company['profitMargins'] * 100:.2f}%"

    price_change(data)
    dailyReturns(data)
    calculate_rsi(data)
    calculate_sma(data,20)
    calculate_ema(data,20)
    calculate_macd(data)
    marking_bs(data)

    mark_signals(data)
    periodicReturns = periodic_returns(data)

    indicators = ["RSI","SMA_20","EMA_20","MACD"]
    graphPlot = generate_graph(data,indicators)

    return render_template("main.html",graph=graphPlot,symbol_name=ticker.info['longName'],
                           tLTP=LTP['tLTP'],percentChange=LTP['percentChange'],
                           currency=ticker.info['currency'],company=company,periodicReturns=periodicReturns)


if __name__ == "__main__":
    app.run(debug=True)