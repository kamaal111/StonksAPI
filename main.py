from fastapi import FastAPI
from datetime import date
import pandas
import yfinance


app = FastAPI()

@app.get("/")
def read_root():
    start_date = pandas.to_datetime('2021-01-01')
    end_date = pandas.to_datetime(date.today())
    aapl = yfinance.download("AAPL", start=start_date, end=end_date, interval="1d")
    return aapl["Close"].to_dict()