from typing import Any


class InvalidQueryParamValueException(Exception):
    def __init__(self, name: str, value: Any):
        self.name = name
        self.value = value
