from datetime import datetime, timedelta

from app.tickers.services.yahoo_finances import YahooFinances
from app.tickers.exceptions import NoCloseDataFound
from app.tickers.responses import InfoResponse


class GetInfoController:
    def __init__(self) -> None:
        pass

    @classmethod
    def get(cls, symbols: str, date: datetime | None):
        symbols_list = symbols.split(",")
        yahoo_finances = YahooFinances()
        if not date or cls.__is_today(date=date):
            return cls.__get_info_for_today(
                yahoo_finances=yahoo_finances, symbols_list=symbols_list
            )

        # start date 3 days ago to include weekdays in case of the date being a Sunday
        start_date = date - timedelta(days=3)
        symbols_closes = yahoo_finances.get_closes(
            symbols=symbols_list,
            start_date=start_date,
            end_date=date,
            interval="1d",
        )
        response: [str, InfoResponse] = {}
        for symbol in symbols_list:
            currency = yahoo_finances.get_currency(symbol=symbol)
            if currency is None:
                continue

            try:
                closes = symbols_closes[symbol]
            except KeyError:
                continue

            close_date = sorted(closes.keys())[-1]
            response[symbol] = InfoResponse(
                name=yahoo_finances.get_long_name(symbol=symbol),
                close=closes[close_date],
                currency=currency,
                close_date=close_date,
            )

        if len(response) == 0:
            raise NoCloseDataFound(symbol=symbols)

        return response

    @classmethod
    def __get_info_for_today(
        cls, yahoo_finances: YahooFinances, symbols_list: list[str]
    ):
        response: [str, InfoResponse] = {}
        closes = yahoo_finances.get_previous_closes(symbols=symbols_list)
        for symbol in symbols_list:
            currency = yahoo_finances.get_currency(symbol=symbol)
            if currency is None:
                continue

            try:
                response[symbol] = InfoResponse(
                    name=yahoo_finances.get_long_name(symbol=symbol),
                    close=closes[symbol],
                    currency=currency,
                    close_date=None,
                )
            except KeyError:
                continue

        if len(response) == 0:
            raise NoCloseDataFound(symbol=",".join(symbols_list))

        return response

    @staticmethod
    def __is_today(date: datetime):
        return datetime.today().date() == date.date()
