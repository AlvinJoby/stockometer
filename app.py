from flask import Flask,render_template,request
from validation import validateInput
from retrieveData import retrieve_data
from graph import generate_graph
import pandas as pd


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/analyze',  methods=['POST'])
def analyze():
    symbol = request.form.get("symbol")
    start_date = request.form.get("start_date") 
    end_date = request.form.get("end_date")
    print(symbol," ",start_date," ",end_date)

    validation_result = validateInput(symbol,start_date,end_date)
    

    if not validation_result["status"]:
        return validation_result["error"]
    
    data = retrieve_data(symbol,start_date,end_date)
    graphPlot = generate_graph(data,symbol)

    return render_template("main.html",graph=graphPlot)


if __name__ == "__main__":
    app.run(debug=True)