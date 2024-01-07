from datetime import datetime
from typing import TYPE_CHECKING, Optional
from app.tickers.configuration import DEFAULT_SUPPORTED_INTERVAL
from app.tickers.exceptions import NoCloseDataFound

from app.tickers.services.yahoo_finances import YahooFinances


if TYPE_CHECKING:
    from app.tickers.configuration import SupportedIntervals


class GetClosesController:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get(
        symbol: str,
        interval: Optional["SupportedIntervals"],
        start_date: datetime | None,
        end_date: datetime | None,
    ):
        yahoo_finances = YahooFinances()
        closes = yahoo_finances.get_closes(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date or datetime.now(),
            interval=interval or DEFAULT_SUPPORTED_INTERVAL,
        )
        if closes is None:
            raise NoCloseDataFound(symbol=symbol)

        return closes
