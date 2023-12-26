from typing import Literal, get_args


SupportedIntervals = Literal[
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

DEFAULT_SUPPORTED_INTERVAL: SupportedIntervals = "1d"


SUPPORTED_INTERVALS: list[SupportedIntervals] = list(get_args(SupportedIntervals))
