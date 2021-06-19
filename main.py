from typing import Any, Dict, Optional
from fastapi import FastAPI, HTTPException
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


def process_ticker(ticker: Any, ticker_key: str, end_date: Optional[datetime], close_date: datetime):
    if ticker_key == "SYMBOL":
        return None
    info = ticker.info
    close = info.get("previousClose", None)
    if end_date is not None:
        start_date = close_date - timedelta(days=3)
        closes_data = ticker.history(start=start_date, end=end_date, interval="1d")["Close"]
        closes_dict = closes_data.to_dict()
        closes_time_stamps = closes_dict.keys()
        if len(closes_time_stamps) > 0:
            last_close = closes_dict[max(closes_time_stamps)]
            close = last_close
    if close is None:
        return None
    logo_url =  info.get("logo_url", None)
    if logo_url == "":
        logo_url = None
    return {
        "logo_url": logo_url,
        "short_name": info.get("shortName", None),
        "long_name": info.get("longName", None),
        "close": close,
        "currency": info.get("currency", None),
        "symbol": ticker_key
    }


def get_info_response(symbol: str, close_date: Optional[str]):
    response = {}
    end_date = None
    if close_date is not None and close_date != "":
        try:
            close_date = datetime.strptime(close_date, '%Y-%m-%d')
        except ValueError:
            close_date = datetime.today()
        end_date = close_date
    for (ticker_key, ticker) in yfinance.Tickers(symbol).tickers.items():
        response_info = process_ticker(ticker=ticker, ticker_key=ticker_key, end_date=end_date, close_date=close_date)
        if response_info is not None:
            response[ticker_key] = response_info
    return response


class InfoModel(BaseModel):
    logo_url: Optional[str]
    short_name: Optional[str]
    long_name: Optional[str]
    close: float
    currency: Optional[str]
    symbol: str


@app.get("/info/{symbol}", response_model=Dict[str, InfoModel])
def get_info(symbol: str, close_date: Optional[str] = None):
    response = get_info_response(symbol=symbol, close_date=close_date)
    if len(response) == 0:
        raise HTTPException(status_code=404, detail="No items found")
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
