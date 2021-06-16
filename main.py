from typing import Dict, Optional
from fastapi import FastAPI
from datetime import date, timedelta, datetime
from pydantic import BaseModel
import yfinance


SUPPORTED_INTERVALS = ["1m", "2m", "5m", "15m", "30m", "60m", 
                        "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]


app = FastAPI()

class RootModel(BaseModel):
    hello: str


@app.get("/", response_model=RootModel)
def get_root():
    return {
        "hello": "welcome"
    }


class InfoModel(BaseModel):
    logo_url: Optional[str]
    short_name: Optional[str]
    long_name: Optional[str]
    previous_close: Optional[float]
    currency: Optional[str]


@app.get("/info/{symbol}", response_model=Dict[str, InfoModel])
def get_info(symbol: str):
    response = {}
    for (ticker_key, ticker) in yfinance.Tickers(symbol).tickers.items():
        info = ticker.info
        response_info = {
            "logo_url": info.get("logo_url", None),
            "short_name": info.get("shortName", None),
            "long_name": info.get("longName", None),
            "previous_close": info.get("previousClose", None),
            "currency": info.get("currency", None)
        }
        response[ticker_key] = response_info

    return response


@app.get("/close/{symbol}", response_model=Dict[str, Dict[datetime, float]])
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
