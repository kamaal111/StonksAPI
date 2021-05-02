from typing import Optional
from fastapi import FastAPI
from datetime import date, timedelta, datetime
import pandas
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
        start_date = pandas.to_datetime(date.today() - timedelta(days=3))
    end_date = pandas.to_datetime(date.today())

    if interval not in SUPPORTED_INTERVALS:
        interval = "1d"

    aapl = yfinance.download(quote, start=start_date, end_date=end_date, interval=interval)

    return aapl["Close"].to_dict()