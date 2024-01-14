from datetime import datetime
from typing import TYPE_CHECKING, Optional
from app.tickers.configuration import DEFAULT_SUPPORTED_INTERVAL
from app.tickers.exceptions import NoCloseDataFound
from app.tickers.responses import ClosesResponse

from app.tickers.services.yahoo_finances import YahooFinances


if TYPE_CHECKING:
    from app.tickers.configuration import SupportedIntervals


class GetClosesController:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get(
        symbols: str,
        interval: Optional["SupportedIntervals"],
        start_date: datetime | None,
        end_date: datetime | None,
    ):
        symbols_list = symbols.split(",")
        yahoo_finances = YahooFinances()
        currencies = yahoo_finances.get_currencies(symbols=symbols_list)
        if currencies is None or len(currencies) == 0:
            raise NoCloseDataFound(symbol=symbols)

        closes = yahoo_finances.get_closes(
            symbols=symbols_list,
            start_date=start_date,
            end_date=end_date or datetime.now(),
            interval=interval or DEFAULT_SUPPORTED_INTERVAL,
        )
        if len(closes) == 0:
            raise NoCloseDataFound(symbol=symbols)

        response: dict[str, ClosesResponse] = {}
        for symbol in symbols_list:
            try:
                response[symbol] = ClosesResponse(
                    closes=closes[symbol], currency=currencies[symbol]
                )
            except KeyError:
                continue
        return response
