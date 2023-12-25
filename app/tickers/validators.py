from datetime import datetime
from typing import Any, Callable

from app.exceptions.exceptions import InvalidQueryParamValueException

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


class InvalidDateException(Exception):
    ...


class InvalidIntervalException(Exception):
    ...


def is_valid_history_interval(value: Any) -> str:
    if not value:
        return "1d"

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
    except ValueError:
        raise InvalidDateException()


def validate_query_param(named: str, validator: Callable):
    def func(value: Any):
        try:
            return validator(value)
        except Exception:
            raise InvalidQueryParamValueException(name=named, value=value)

    return func
