from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from app.exceptions.exceptions import InvalidQueryParamValueException

from app.health.router import router as health_router
from app.tickers.router import router as tickers_router


app = FastAPI()


@app.exception_handler(InvalidQueryParamValueException)
async def unicorn_exception_handler(_, exc: InvalidQueryParamValueException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": f"Invalid query param for '{exc.name}' with value '{exc.value}'"
        },
    )


app.include_router(health_router)
app.include_router(tickers_router)
