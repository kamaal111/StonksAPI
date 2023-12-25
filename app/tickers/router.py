from datetime import date, datetime, timedelta
from fastapi import APIRouter, HTTPException, status
from pydantic import StringConstraints
from pydantic.functional_validators import BeforeValidator
from typing import Annotated

from app.exceptions.responses import ExceptionResponse
from app.tickers.responses import InfoResponse
from app.tickers.services.yahoo_finances import YahooFinances
from app.tickers.validators import (
    is_valid_history_interval,
    valid_date_or_none,
    validate_query_param,
)

router = APIRouter(tags=["tickers"], prefix="/tickers")


@router.get(
    "/info/{symbol}",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
    },
)
def get_info(
    symbol: Annotated[str, StringConstraints(min_length=1)],
    close_date: Annotated[
        datetime,
        BeforeValidator(validate_query_param("close_date", valid_date_or_none)),
    ] = None,
) -> InfoResponse:
    formatted_final_close_date = None
    ticker = YahooFinances.get_ticker(symbol=symbol)
    if not ticker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No information found for {symbol}",
        )

    info = ticker.info
    close = info.get("previousClose", None)
    if close_date:
        start_date = close_date - timedelta(days=3)
        closes_data = ticker.history(start=start_date, end=close_date, interval="1d")[
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

    if close is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No close found for {symbol}",
        )

    return InfoResponse(
        name=info.get("longName", None),
        close=close,
        currency=info.get("currency", None),
        symbol=symbol,
        close_date=formatted_final_close_date,
    )


@router.get(
    "/close/{symbol}",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
    },
)
def get_close(
    symbol: str,
    interval: Annotated[
        str,
        BeforeValidator(validate_query_param("interval", is_valid_history_interval)),
    ] = None,
    start_date: Annotated[
        datetime,
        BeforeValidator(validate_query_param("start_date", valid_date_or_none)),
    ] = None,
) -> dict[str, float]:
    ticker = YahooFinances.get_ticker(symbol=symbol)
    if not ticker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No information found for {symbol}",
        )

    close_series = ticker.history(
        start=start_date, end=date.today(), interval=interval
    )["Close"]

    response = {}
    for close_date, close_value in close_series.to_dict().items():
        close_date = datetime.utcfromtimestamp(
            close_date.value / 1_000_000_000
        ).isoformat()
        response[close_date] = close_value
    return response
