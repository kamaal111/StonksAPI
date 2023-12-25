from datetime import date, datetime, timedelta
from fastapi import APIRouter, HTTPException, status
import yfinance

from app.exceptions.exceptions import InvalidQueryParamValueException
from app.exceptions.responses import ExceptionResponse
from app.tickers.responses import InfoResponse

router = APIRouter(tags=["tickers"], prefix="/tickers")


SUPPORTED_INTERVALS = [
    "1m",
    "2m",
    "5m",
    "15m",
    "30m",
    "60m",
    "90m",
    "1h",
    "1d",
    "5d",
    "1wk",
    "1mo",
    "3mo",
]


@router.get(
    "/info/{symbol}",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
    },
)
def get_info(symbol: str, close_date: str | None = None) -> InfoResponse:
    end_date = None
    if close_date:
        try:
            close_date = datetime.strptime(close_date, "%Y-%m-%d")
        except ValueError:
            raise InvalidQueryParamValueException(name="close_date", value=close_date)
        end_date = close_date

    final_close_date = None
    for ticker_key, ticker in yfinance.Tickers(symbol).tickers.items():
        if ticker_key != symbol:
            continue

        info = ticker.info
        close = info.get("previousClose", None)
        if end_date:
            start_date = close_date - timedelta(days=3)
            closes_data = ticker.history(start=start_date, end=end_date, interval="1d")[
                "Close"
            ]
            closes_dict = closes_data.to_dict()
            closes_time_stamps = closes_dict.keys()
            final_close_date = max(closes_time_stamps)
            if len(closes_time_stamps) > 0:
                last_close = closes_dict[final_close_date]
                close = last_close

        if close is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No close found for {symbol}",
            )
        assert final_close_date is not None

        return InfoResponse(
            name=info.get("longName", None),
            close=close,
            currency=info.get("currency", None),
            symbol=symbol,
            close_date=datetime.utcfromtimestamp(
                final_close_date.value / 1_000_000_000
            ).isoformat(),
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No information found for {symbol}",
    )


@router.get(
    "/close/{symbol}",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
    },
)
def get_close(
    symbol: str, interval: str = None, start_date: str = None
) -> dict[str, float]:
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        raise InvalidQueryParamValueException(name="start_date", value=start_date)
    end_date = date.today()

    if interval is None:
        interval = "1d"

    if interval not in SUPPORTED_INTERVALS:
        raise InvalidQueryParamValueException(name="interval", value=interval)

    for ticker_key, ticker in yfinance.Tickers(symbol).tickers.items():
        if ticker_key != symbol:
            continue

        close_series = ticker.history(
            start=start_date, end=end_date, interval=interval
        )["Close"]

        response = {}
        for close_date, close_value in close_series.to_dict().items():
            close_date = datetime.utcfromtimestamp(
                close_date.value / 1_000_000_000
            ).isoformat()
            response[close_date] = close_value
        return response

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No information found for {symbol}",
    )
