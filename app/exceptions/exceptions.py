from fastapi import HTTPException, status
from typing import Any


class InvalidQueryParamValueException(HTTPException):
    def __init__(self, name: str, value: Any):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid query param for {name=} with {value=}",
        )
