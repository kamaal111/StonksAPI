from datetime import datetime, timedelta
from app.tickers.exceptions import NoCloseDataFound, TickerNotFoundException
from app.tickers.responses import InfoResponse

from app.tickers.services.yahoo_finances import YahooFinances


class GetInfoController:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get(symbol: str, date: datetime | None):
        ticker = YahooFinances.get_ticker(symbol=symbol)
        if not ticker:
            raise TickerNotFoundException(symbol=symbol)

        try:
            info = ticker.info
        except Exception:
            raise TickerNotFoundException(symbol=symbol)

        if date:
            start_date = date - timedelta(days=3)
            closes_data = ticker.history(start=start_date, end=date, interval="1d")[
                "Close"
            ]
            closes_dict = closes_data.to_dict()
            closes_time_stamps = closes_dict.keys()
            final_close_date = max(closes_time_stamps)
            if len(closes_time_stamps) > 0:
                last_close = closes_dict[final_close_date]
                close = last_close

            formatted_final_close_date = datetime.utcfromtimestamp(
                final_close_date.value / 1_000_000_000
            ).isoformat()
        else:
            close = info.get("previousClose", None)

        if close is None:
            raise NoCloseDataFound(symbol=symbol)

        return InfoResponse(
            name=info.get("longName", None),
            close=close,
            currency=info.get("currency", None),
            symbol=symbol,
            close_date=formatted_final_close_date,
        )
