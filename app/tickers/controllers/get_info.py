from datetime import datetime, timedelta

from app.tickers.services.yahoo_finances import YahooFinances
from app.tickers.exceptions import NoCloseDataFound, TickerNotFoundException
from app.tickers.responses import InfoResponse


class GetInfoController:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get(symbol: str, date: datetime | None):
        yahoo_finances = YahooFinances()
        name = yahoo_finances.get_long_name(symbol=symbol)
        currency = yahoo_finances.get_currency(symbol=symbol)
        if not currency:
            raise TickerNotFoundException(symbol=symbol)

        if not date:
            close = yahoo_finances.get_previous_close(symbol=symbol)
            if not close:
                raise TickerNotFoundException(symbol=symbol)

            return InfoResponse(
                name=name,
                close=close,
                currency=currency,
                symbol=symbol,
                close_date=None,
            )

        # start date 3 days ago to include weekdays in case of the date being a Sunday
        start_date = date - timedelta(days=3)
        closes = yahoo_finances.get_closes(
            symbol=symbol,
            start_date=start_date,
            end_date=date,
            interval="1d",
        )
        if closes is None or len(closes) == 0:
            raise NoCloseDataFound(symbol=symbol)

        close_date = sorted(closes.keys())[-1]
        close: float = closes[close_date]

        return InfoResponse(
            name=name,
            close=close,
            currency=currency,
            symbol=symbol,
            close_date=close_date,
        )
