from typing import Optional
from fastapi import FastAPI
from datetime import date
import pandas
import yfinance


SUPPORTED_INTERVALS = ["1m", "2m", "5m", "15m", "30m", "60m", 
                        "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/quote/{quote}")
def read_item(quote: str, interval: Optional[str] = None):
    start_date = pandas.to_datetime('2021-01-01')
    end_date = pandas.to_datetime(date.today())
    user_defined_interval = "1d"
    if interval in SUPPORTED_INTERVALS:
        user_defined_interval = interval
    aapl = yfinance.download(quote, start=start_date, end=end_date, interval=user_defined_interval)

    return aapl["Close"].to_dict()