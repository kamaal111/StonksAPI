FROM python:3.12-slim-bookworm AS builder

RUN pip install poetry
RUN python -m venv .venv
RUN . .venv/bin/activate
COPY poetry.lock pyproject.toml ./
RUN poetry install --without dev

RUN apt update && apt install -y \
    tzdata ca-certificates

FROM python:3.12-slim-bookworm

COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder .venv .venv
COPY app app

EXPOSE 8000

CMD [".venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
