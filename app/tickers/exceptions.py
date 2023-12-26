from fastapi import HTTPException, status


class TickerNotFoundException(HTTPException):
    def __init__(self, symbol: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No information found for {symbol=}",
        )


class NoCloseDataFound(HTTPException):
    def __init__(self, symbol: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No close found for {symbol=}",
        )
