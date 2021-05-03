from typing import Optional
from fastapi import FastAPI
from datetime import date, timedelta, datetime
from time import perf_counter
import yfinance


SUPPORTED_INTERVALS = ["1m", "2m", "5m", "15m", "30m", "60m", 
                        "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/info/{symbol}")
def get_info(symbol: str):
    response = {}
    for (ticker_key, ticker) in yfinance.Tickers(symbol).tickers.items():
        info = ticker.info
        response_info = {}
        response_info["logo_url"] = info["logo_url"]
        response_info["previous_close"] = info["previousClose"]
        response_info["short_name"] = info["shortName"]
        response_info["long_name"] = info["longName"]
        response[ticker_key] = response_info

    return response

@app.get("/close/{symbol}")
def get_close(symbol: str, interval: Optional[str] = "1d", start_date: Optional[str] = ""):
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError:
        start_date = datetime.today() - timedelta(days=3)
    end_date = date.today()

    if interval not in SUPPORTED_INTERVALS:
        interval = "1d"

    response = {}
    for (ticker_key, ticker) in yfinance.Tickers(symbol).tickers.items():
        close = ticker.history(start=start_date, end=end_date, interval=interval)["Close"]
        response[ticker_key] = close.to_dict()

    return response
