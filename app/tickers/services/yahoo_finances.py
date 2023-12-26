from dataclasses import dataclass
from typing import TYPE_CHECKING, Any


from yfinance import Tickers

from datetime import datetime, date as datetime_date


if TYPE_CHECKING:
    from pandas import DataFrame
    from yfinance import Ticker

    from app.tickers.configuration import SupportedIntervals


Date = datetime | datetime_date


@dataclass
class RequestTicker:
    ticker: "Ticker"
    info: dict | None
    history: dict[str, "DataFrame"]


class YahooFinances:
    request_tickers: dict[str, RequestTicker]

    def __init__(self) -> None:
        self.request_tickers = {}

    def get_info(self, symbol: str):
        request_ticker = self.__get_request_ticker(symbol=symbol)
        if not request_ticker:
            return None

        if info := request_ticker.info:
            return info

        try:
            info = request_ticker.ticker.info
        except Exception:
            return None

        self.request_tickers[symbol].info = info
        return info

    def get_long_name(self, symbol: str):
        return self.__get_info_value(symbol=symbol, key="longName")

    def get_currency(self, symbol: str):
        return self.__get_info_value(symbol=symbol, key="currency")

    def get_previous_close(self, symbol: str) -> float | None:
        if info := self.get_info(symbol=symbol):
            return info.get("previousClose", None)

    def get_closes(
        self,
        symbol: str,
        start_date: Date | None,
        end_date: Date,
        interval: "SupportedIntervals",
    ):
        return self.__get_history_values(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            interval=interval,
            key="Close",
        )

    def __get_info_value(self, symbol: str, key: str):
        if info := self.get_info(symbol=symbol):
            return info.get(key)

    def __get_history(
        self,
        symbol: str,
        start_date: Date | None,
        end_date: Date,
        interval: "SupportedIntervals",
    ):
        request_ticker = self.__get_request_ticker(symbol=symbol)
        if not request_ticker:
            return None

        history_key = self.__make_history_key(
            start_date=start_date, end_date=end_date, interval=interval
        )
        if (histories := request_ticker.history) and (
            history := histories.get(history_key)
        ):
            return history

        history = request_ticker.ticker.history(
            start=start_date, end=end_date, interval=interval
        )
        if self.request_tickers[symbol].history is None:
            self.request_tickers[symbol].history = {history_key: history}
        else:
            self.request_tickers[symbol].history[history_key] = history
        return history

    def __make_history_key(
        self, start_date: Date | None, end_date: Date, interval: "SupportedIntervals"
    ):
        start_date_key = start_date.timestamp() if start_date is not None else "None"
        return f"{start_date_key}-{end_date.timestamp()}-{interval}"

    def __get_history_values(
        self,
        symbol: str,
        start_date: Date | None,
        end_date: Date,
        interval: "SupportedIntervals",
        key: str,
    ):
        history = self.__get_history(
            symbol=symbol, start_date=start_date, end_date=end_date, interval=interval
        )
        if history is None:
            return None

        close_series = history[key]
        if close_series.empty:
            return None

        closes: dict[str, Any] = {}
        for close_date, close_value in close_series.items():
            close_date = datetime.utcfromtimestamp(
                close_date.value / 1_000_000_000
            ).isoformat()
            closes[close_date] = close_value

        return closes

    def __get_request_ticker(self, symbol: str):
        if request_ticker := self.request_tickers.get(symbol):
            return request_ticker

        for ticker_key, ticker in Tickers(symbol).tickers.items():
            self.request_tickers[ticker_key] = RequestTicker(
                ticker=ticker, info=None, history=None
            )

        return self.request_tickers.get(symbol)
