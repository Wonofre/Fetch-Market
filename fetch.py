from flask import Flask, jsonify, request, Response
import yfinance as yf
from datetime import datetime
import os
import pandas as pd

app = Flask(__name__)

def fetch_historical_data(symbol, start_date, end_date):
    ticker = yf.Ticker(symbol)
    historical_data = ticker.history(start=start_date, end=end_date)
    return historical_data

@app.route('/historical_data', methods=['GET'])
def get_historical_data():
    symbol = request.args.get('symbol', default='AAPL', type=str)
    start_date = request.args.get('start', default=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'), type=str)
    end_date = request.args.get('end', default=datetime.now().strftime('%Y-%m-%d'), type=str)
    data = fetch_historical_data(symbol, start_date, end_date)
    return jsonify(data.to_json())

@app.route('/historical_data_csv', methods=['GET'])
def get_historical_data_csv():
    symbol = request.args.get('symbol', default='AAPL', type=str)
    start_date = request.args.get('start', default=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'), type=str)
    end_date = request.args.get('end', default=datetime.now().strftime('%Y-%m-%d'), type=str)
    data = fetch_historical_data(symbol, start_date, end_date)
    csv_data = data.to_csv(index=False)
    return Response(csv_data, mimetype='text/csv', headers={"Content-disposition": f"attachment; filename={symbol}_historical_data.csv"})

@app.route('/')
def home():
    return "Welcome to the Stock Data API! Use /historical_data?symbol=SYMBOL&start=START_DATE&end=END_DATE to fetch data in JSON format, or /historical_data_csv?symbol=SYMBOL&start=START_DATE&end=END_DATE to fetch data in CSV format."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

