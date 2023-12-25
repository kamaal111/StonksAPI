from pydantic import BaseModel


class InfoResponse(BaseModel):
    name: str | None
    close: float
    currency: str | None
    symbol: str
    close_date: str | None
