from flask import Flask, jsonify, request
import yfinance as yf
from datetime import datetime, timedelta
import os

app = Flask(__name__)

def fetch_historical_data(symbol):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)  # Last three months
    ticker = yf.Ticker(symbol)
    historical_data = ticker.history(start=start_date, end=end_date)
    return historical_data.to_json()

@app.route('/historical_data', methods=['GET'])
def get_historical_data():
    symbol = request.args.get('symbol', default='AAPL', type=str)
    data = fetch_historical_data(symbol)
    return jsonify(data)

@app.route('/')
def home():
    return "Welcome to the Stock Data API! Use /historical_data?symbol=SYMBOL to fetch data."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Heroku will supply the PORT environment variable
    app.run(host='0.0.0.0', port=port, debug=False)  # Turn off debug mode when deploying to production

