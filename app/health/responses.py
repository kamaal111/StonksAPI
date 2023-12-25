from typing import Literal
from pydantic import BaseModel


class PingResponse(BaseModel):
    message: Literal["pong"]
