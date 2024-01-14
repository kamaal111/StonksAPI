from datetime import datetime
from fastapi import APIRouter, status
from pydantic import StringConstraints
from pydantic.functional_validators import BeforeValidator
from typing import Annotated

from app.exceptions.responses import ExceptionResponse
from app.tickers.controllers.get_closes import GetClosesController
from app.tickers.controllers.get_info import GetInfoController
from app.tickers.responses import ClosesResponse, InfoResponse
from app.tickers.validators import (
    is_valid_history_interval,
    valid_date_or_none,
    validate_query_param,
)

router = APIRouter(tags=["tickers"], prefix="/tickers")


@router.get(
    "/info",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
    },
    response_model=dict[str, InfoResponse],
)
def get_info(
    symbols: Annotated[str, StringConstraints(min_length=1)],
    date: Annotated[
        datetime | None,
        BeforeValidator(validate_query_param("date", valid_date_or_none)),
    ] = None,
):
    return GetInfoController.get(symbols=symbols, date=date)


@router.get(
    "/closes",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
    },
    response_model=dict[str, ClosesResponse],
)
def get_close(
    symbols: Annotated[str, StringConstraints(min_length=1)],
    interval: Annotated[
        str | None,
        BeforeValidator(validate_query_param("interval", is_valid_history_interval)),
    ] = None,
    start_date: Annotated[
        datetime | None,
        BeforeValidator(validate_query_param("start_date", valid_date_or_none)),
    ] = None,
    end_date: Annotated[
        datetime | None,
        BeforeValidator(validate_query_param("end_date", valid_date_or_none)),
    ] = None,
):
    return GetClosesController.get(
        symbols=symbols, interval=interval, start_date=start_date, end_date=end_date
    )
