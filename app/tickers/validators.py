from datetime import datetime
from typing import TYPE_CHECKING, Any, Callable, Optional

from app.exceptions.exceptions import InvalidQueryParamValueException
from app.tickers.configuration import SUPPORTED_INTERVALS


if TYPE_CHECKING:
    from app.tickers.configuration import SupportedIntervals


class InvalidDateException(Exception):
    ...


class InvalidIntervalException(Exception):
    ...


def is_valid_history_interval(value: Any) -> Optional["SupportedIntervals"]:
    if not value:
        return None

    if value not in SUPPORTED_INTERVALS:
        raise InvalidIntervalException()

    return value


def valid_date_or_none(value: Any | None):
    if not value:
        return None

    if not isinstance(value, str):
        raise InvalidDateException()

    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError as e:
        raise InvalidDateException() from e


def validate_query_param(named: str, validator: Callable):
    def func(value: Any):
        try:
            return validator(value)
        except Exception as e:
            raise InvalidQueryParamValueException(name=named, value=value) from e

    return func
