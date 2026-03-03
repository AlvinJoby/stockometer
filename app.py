from flask import Flask,render_template,request
from validation import validateInput
from retrieveData import retrieve_data,retrieve_ltp,retrieve_companyInfo
from graph import generate_graph
from analysis.company_data import companyData,format_large_number
import pandas as pd


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
    graphPlot = generate_graph(data,symbol)

    LTP = retrieve_ltp(data,symbol)
    ticker = retrieve_companyInfo(symbol)
    company= companyData(ticker)

    company["marketCap"] = format_large_number(company["marketCap"])
    company["totalRevenue"] = format_large_number(company["totalRevenue"])
    company["netIncomeToCommon"] = format_large_number(company["netIncomeToCommon"])
    company["profitMargins"] = f"{company['profitMargins'] * 100:.2f}%"

    return render_template("main.html",graph=graphPlot,symbol_name=ticker.info['longName'],
                           tLTP=LTP['tLTP'],percentChange=LTP['percentChange'],
                           currency=ticker.info['currency'],company=company)


if __name__ == "__main__":
    app.run(debug=True)