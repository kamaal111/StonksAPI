from datetime import date as datetime_date, datetime
from fastapi import APIRouter, HTTPException, status
from pydantic import StringConstraints
from pydantic.functional_validators import BeforeValidator
from typing import Annotated

from app.exceptions.responses import ExceptionResponse
from app.tickers.controllers.get_info import GetInfoController
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
    response_model=InfoResponse,
)
def get_info(
    symbol: Annotated[str, StringConstraints(min_length=1)],
    date: Annotated[
        datetime | None,
        BeforeValidator(validate_query_param("date", valid_date_or_none)),
    ] = None,
):
    return GetInfoController.get(symbol=symbol, date=date)


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
        datetime | None,
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
        start=start_date, end=datetime_date.today(), interval=interval
    )["Close"]

    response = {}
    for close_date, close_value in close_series.to_dict().items():
        close_date = datetime.utcfromtimestamp(
            close_date.value / 1_000_000_000
        ).isoformat()
        response[close_date] = close_value
    return response
