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
        yahoo_finances = YahooFinances()
        symbols_list = symbols.split(",")
        closes = yahoo_finances.get_closes(
            symbols=symbols_list,
            start_date=start_date,
            end_date=end_date or datetime.now(),
            interval=interval or DEFAULT_SUPPORTED_INTERVAL,
        )
        response: dict[str, ClosesResponse] = {}
        for symbol in symbols_list:
            currency = yahoo_finances.get_currency(symbol=symbol)
            if currency is None:
                raise NoCloseDataFound(symbol=symbols)

            try:
                response[symbol] = ClosesResponse(
                    closes=closes[symbol], currency=currency
                )
            except KeyError:
                continue
        return response
