set export

VIRTUAL_ENVIRONMENT := ".venv"
CONTAINER_NAME := "stonks-api"
PORT := "8000"

build-run: build run

run: stop-and-remove-container
    docker run -dp $PORT:$PORT --name $CONTAINER_NAME -e PORT=$PORT $CONTAINER_NAME

build:
    docker build -t $CONTAINER_NAME .

run-dev:
    #!/bin/zsh

    just install-python-packages
    . $VIRTUAL_ENVIRONMENT/bin/activate
    uvicorn app.main:app --reload

bootstrap: setup-python-environment

[private]
stop-and-remove-container:
    docker stop $CONTAINER_NAME || true
    docker rm $CONTAINER_NAME || true

[private]
setup-python-environment:
    #!/bin/zsh

    if [ ! -d $VIRTUAL_ENVIRONMENT ]
    then
        python3 -m venv $VIRTUAL_ENVIRONMENT
    fi
    . $VIRTUAL_ENVIRONMENT/bin/activate
    pip install --upgrade pip
    pip install poetry
    just install-python-packages
    pre-commit install

[private]
install-python-packages:
    #!/bin/zsh

    . $VIRTUAL_ENVIRONMENT/bin/activate
    poetry install --no-root
