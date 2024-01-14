from dataclasses import dataclass
from typing import TYPE_CHECKING, Any


from yfinance import Tickers

from datetime import datetime


if TYPE_CHECKING:
    from pandas import DataFrame
    from yfinance import Ticker

    from app.tickers.configuration import SupportedIntervals


@dataclass
class RequestTicker:
    ticker: "Ticker"
    info: dict | None
    history: dict[str, "DataFrame"]


class YahooFinances:
    request_tickers: dict[str, RequestTicker]

    def __init__(self) -> None:
        self.request_tickers = {}

    def get_long_name(self, symbol: str) -> str | None:
        return self.__get_info_values(symbols=[symbol], key="longName").get(symbol)

    def get_currency(self, symbol: str) -> str | None:
        return self.__get_info_values(symbols=[symbol], key="currency").get(symbol)

    def get_currencies(self, symbols: list[str]) -> dict[str, str] | None:
        return self.__get_info_values(symbols=symbols, key="currency")

    def get_previous_close(self, symbol: str) -> float | None:
        return self.__get_infos(symbols=[symbol]).get(symbol, {}).get("previousClose")

    def get_closes(
        self,
        symbols: list[str],
        start_date: datetime | None,
        end_date: datetime,
        interval: "SupportedIntervals",
    ):
        return self.__get_history_values(
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            interval=interval,
            key="Close",
        )

    def __get_infos(self, symbols: list[str]):
        request_tickers = self.__get_request_tickers(symbols=symbols)
        infos: dict[str, dict] = {}
        for symbol, request_ticker in request_tickers.items():
            if info := request_ticker.info:
                infos[symbol] = info
                continue

            try:
                info = request_ticker.ticker.info
            except Exception:
                continue

            self.request_tickers[symbol].info = info
            infos[symbol] = info

        return infos

    def __get_info_values(self, symbols: list[str], key: str):
        values: dict[str, Any] = {}
        self.__get_infos(symbols=symbols)
        for symbol, info in self.__get_infos(symbols=symbols).items():
            if value := info.get(key):
                values[symbol] = value
        return values

    def __get_histories(
        self,
        symbols: list[str],
        start_date: datetime | None,
        end_date: datetime,
        interval: "SupportedIntervals",
    ):
        request_tickers = self.__get_request_tickers(symbols=symbols)
        histories: dict[str, "DataFrame"] = {}
        for symbol, request_ticker in request_tickers.items():
            history_key = self.__make_history_key(
                start_date=start_date, end_date=end_date, interval=interval
            )
            if (request_ticker_history := request_ticker.history) and (
                history := request_ticker_history.get(history_key)
            ):
                histories[symbol] = history
                continue

            history = request_ticker.ticker.history(
                start=start_date, end=end_date, interval=interval
            )
            histories[symbol] = history
            if self.request_tickers[symbol].history is None:
                self.request_tickers[symbol].history = {history_key: history}
            else:
                self.request_tickers[symbol].history[history_key] = history

        return histories

    def __make_history_key(
        self,
        start_date: datetime | None,
        end_date: datetime,
        interval: "SupportedIntervals",
    ):
        start_date_key = start_date.timestamp() if start_date is not None else "None"
        return f"{start_date_key}-{end_date.timestamp()}-{interval}"

    def __get_history_values(
        self,
        symbols: list[str],
        start_date: datetime | None,
        end_date: datetime,
        interval: "SupportedIntervals",
        key: str,
    ):
        histories = self.__get_histories(
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            interval=interval,
        )
        history_values: dict[str, dict[str, Any]] = {}
        for symbol, history in histories.items():
            series = history[key]
            if series.empty:
                continue

            values_dict: dict[str, Any] = {}
            for timestamp, value in series.items():
                timestamp_datetime = datetime.utcfromtimestamp(
                    timestamp.value / 1_000_000_000
                ).isoformat()
                values_dict[timestamp_datetime] = value

            history_values[symbol] = values_dict

        return history_values

    def __get_request_tickers(self, symbols: list[str]):
        cached_tickers: dict[str, RequestTicker] = {}
        symbols_set = set(symbols)
        for symbol in symbols_set:
            if request_ticker := self.request_tickers.get(symbol):
                cached_tickers[symbol] = request_ticker

        cached_symbols = cached_tickers.keys()
        remaining_symbols = list(
            filter(lambda symbol: symbol not in cached_symbols, symbols_set)
        )
        if len(remaining_symbols) == 0:
            return cached_tickers

        request_tickers = cached_tickers
        for ticker_key, ticker in Tickers(",".join(remaining_symbols)).tickers.items():
            request_ticker = RequestTicker(ticker=ticker, info=None, history=None)
            self.request_tickers[ticker_key] = request_ticker
            request_tickers[ticker_key] = request_ticker

        return request_tickers
