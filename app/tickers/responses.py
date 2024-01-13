from pydantic import BaseModel


class InfoResponse(BaseModel):
    name: str | None
    close: float
    currency: str
    symbol: str
    close_date: str | None


class ClosesResponse(BaseModel):
    closes: dict[str, float]
    currency: str
