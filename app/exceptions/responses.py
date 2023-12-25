from pydantic import BaseModel


class ExceptionResponse(BaseModel):
    details: str
