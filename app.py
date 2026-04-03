from flask import Flask, jsonify, render_template, request
from validation import validateInput
from retrieveData import retrieve_data, retrieve_ltp, retrieve_companyInfo, normalize_columns
from graph import generate_graph
from analysis.rsi_indicator import calculate_rsi, mark_signals
from analysis.ma_indicator import calculate_sma, calculate_ema
from analysis.periodic_returns import periodic_returns
from analysis.company_data import companyData, format_number
from analysis.daily_returns import price_change, dailyReturns
from analysis.macd_indicator import calculate_macd
from analysis.buysell_marker import marking_bs
from stockIndex.getIndex import get_index, get_index_display_name
from stockIndex.indexPerformance import index_performance_pipeline
from symbol_search import search_symbols
import pandas as pd

import config


app = Flask(__name__)


def _format_decimal(value, digits=2):
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value:.{digits}f}"


def _format_ratio_as_percent(value, digits=2):
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value * 100:.{digits}f}%"


def _is_greater(left, right):
    if left is None or right is None or pd.isna(left) or pd.isna(right):
        return False
    return left > right


def _prepare_company(symbol, ticker):
    company = companyData(ticker)
    company["longName"] = company.get("longName") or symbol.upper()
    company["marketCap"] = format_number(company.get("marketCap"))
    company["totalRevenue"] = format_number(company.get("totalRevenue"))
    company["netIncomeToCommon"] = format_number(company.get("netIncomeToCommon"))
    company["profitMargins"] = _format_ratio_as_percent(company.get("profitMargins"))

    company["dayHighDisplay"] = _format_decimal(company.get("dayHigh"))
    company["dayLowDisplay"] = _format_decimal(company.get("dayLow"))
    company["fiftyDayAverageDisplay"] = _format_decimal(company.get("fiftyDayAverage"))
    company["fiftyTwoWeekHighDisplay"] = _format_decimal(company.get("fiftyTwoWeekHigh"))
    company["fiftyTwoWeekLowDisplay"] = _format_decimal(company.get("fiftyTwoWeekLow"))
    company["trailingPEDisplay"] = _format_decimal(company.get("trailingPE"))
    company["dividendYieldDisplay"] = _format_ratio_as_percent(company.get("dividendYield"))
    company["betaDisplay"] = _format_decimal(company.get("beta"), digits=3)
    company["priceToBookDisplay"] = _format_decimal(company.get("priceToBook"), digits=3)

    company["isAbove50DayAverage"] = _is_greater(
        company.get("currentPrice"), company.get("fiftyDayAverage"),
    )
    company["isAbove52WeekLow"] = _is_greater(
        company.get("currentPrice"), company.get("fiftyTwoWeekLow"),
    )
    company["hasLowPE"] = (
        company.get("trailingPE") is not None and
        not pd.isna(company.get("trailingPE")) and
        company["trailingPE"] < 25
    )
    company["hasDividend"] = (
        company.get("dividendYield") is not None and
        not pd.isna(company.get("dividendYield")) and
        company["dividendYield"] > 0
    )
    return company


def _clean_series(series):
    return [
        None if (v is None or pd.isna(v)) else round(float(v), 4)
        for v in series
    ]


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/api/symbols')
def symbol_suggestions():
    query = request.args.get("q", "")
    return jsonify(search_symbols(query))


@app.route('/analyze', methods=['POST'])
def analyze():
    symbol = request.form.get("symbol")
    validation_result = validateInput(symbol)

    if not validation_result["status"]:
        return validation_result["error"], 400

    try:
        data = retrieve_data(symbol)
        if data is None or data.empty:
            return "Unable to retrieve price history for the requested symbol.", 502

        data = normalize_columns(data, symbol)

        config.symbol = symbol
        config.data = data

        LTP = retrieve_ltp(data)
        ticker = retrieve_companyInfo(symbol)
        ticker_info = getattr(ticker, "info", {}) or {}
        company = _prepare_company(symbol, ticker)

        price_change(data)
        dailyReturns(data)
        calculate_rsi(data)
        calculate_sma(data, 20)
        calculate_ema(data, 20)
        calculate_ema(data, 50)
        calculate_ema(data, 100)
        calculate_macd(data)
        marking_bs(data)
        mark_signals(data)

        periodicReturns = periodic_returns(data)

        index_summary = None
        index_ts = None
        exchange = ticker_info.get("exchange")
        index = get_index(exchange, symbol)
        index_name = get_index_display_name(index)
        if index:
            index_df = retrieve_data(index)
            if index_df is not None and not index_df.empty:
                index_df = normalize_columns(index_df, index)
                result = index_performance_pipeline(data, index_df)
                df_ts = result.get("timeseries")
                if result.get("summary") is not None and df_ts is not None and not df_ts.empty:
                    index_summary = result["summary"]
                    index_ts = {
                        "dates":             df_ts.index.strftime("%Y-%m-%d").tolist(),
                        "stock_normalized":  _clean_series(df_ts["normalized_stock"]),
                        "index_normalized":  _clean_series(df_ts["normalized_index"]),
                        "alpha_cumulative":  _clean_series(df_ts["alpha_cumulative"]),
                        "alpha_rolling":     _clean_series(df_ts["alpha_rolling"] * 100),
                        "relative_strength": _clean_series(df_ts["relative_strength"]),
                        "rs_ma":             _clean_series(df_ts["rs_ma"]),
                    }

        indicators = ["RSI", "SMA_20", "EMA_20", "EMA_50", "EMA_100", "MACD"]
        graphPlot = generate_graph(data, indicators)

        return render_template(
            "main.html",
            graph=graphPlot,
            symbol_name=ticker_info.get("longName") or company["longName"],
            stock_name=ticker_info.get("shortName") or company["longName"],
            tLTP=LTP["tLTP"],
            percentChange=LTP["percentChange"],
            currency=ticker_info.get("currency", "USD"),
            company=company,
            periodicReturns=periodicReturns,
            summary=index_summary,
            index_ts=index_ts,
            index_name=index_name,
        )
    except ValueError as exc:
        app.logger.exception("Analysis failed for symbol %s", symbol)
        return str(exc), 500
    except Exception:
        app.logger.exception("Unexpected error while analyzing symbol %s", symbol)
        return "Unable to analyze the requested symbol right now.", 500


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
