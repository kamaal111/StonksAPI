from datetime import date as datetime_date, datetime
from app.tickers.exceptions import TickerNotFoundException

from app.tickers.services.yahoo_finances import YahooFinances


class GetCloseController:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get(symbol: str, interval: str, start_date: datetime | None):
        ticker = YahooFinances.get_ticker(symbol=symbol)
        if not ticker:
            raise TickerNotFoundException(symbol=symbol)

        close_series = ticker.history(
            start=start_date, end=datetime_date.today(), interval=interval
        )["Close"]
        response: dict[str, float] = {}
        for close_date, close_value in close_series.to_dict().items():
            close_date = datetime.utcfromtimestamp(
                close_date.value / 1_000_000_000
            ).isoformat()
            response[close_date] = close_value

        return response
