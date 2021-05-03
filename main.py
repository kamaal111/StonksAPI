from typing import Optional
from fastapi import FastAPI
from datetime import date, timedelta, datetime
import yfinance


SUPPORTED_INTERVALS = ["1m", "2m", "5m", "15m", "30m", "60m", 
                        "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/quote/{quote}")
def get_quote_data(quote: str, interval: str = "1d", start_date: str = ""):
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError:
        start_date = date.today() - timedelta(days=3)
    end_date = date.today()

    if interval not in SUPPORTED_INTERVALS:
        interval = "1d"

    response = {}
    for (ticker_key, ticker) in yfinance.Tickers(quote).tickers.items():
        response[ticker_key] = {}
        close = ticker.history(start=start_date, end=end_date, interval=interval)["Close"]
        response[ticker_key]["close"] = close.to_dict()
        info = ticker.info
        response_info = {}
        response_info["logo_url"] = info["logo_url"]
        response_info["previous_close"] = info["previousClose"]
        response_info["short_name"] = info["shortName"]
        response_info["long_name"] = info["longName"]
        response[ticker_key]["info"] = response_info

    return response
