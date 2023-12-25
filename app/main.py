from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.exceptions.exceptions import InvalidQueryParamValueException

from app.health.router import router as health_router
from app.tickers.router import router as tickers_router


app = FastAPI()


@app.exception_handler(InvalidQueryParamValueException)
def invalid_query_param_value_exception_handler(
    _, exc: InvalidQueryParamValueException
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": f"Invalid query param for '{exc.name}' with value '{exc.value}'"
        },
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(_, exc: RequestValidationError):
    errors = exc.errors()
    if len(errors) == 0:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Something went wrong"},
        )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": errors[0]["msg"]},
    )


app.include_router(health_router)
app.include_router(tickers_router)
