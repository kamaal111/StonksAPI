set export

VIRTUAL_ENVIRONMENT := ".venv"
CONTAINER_NAME := "stonks-api"
PORT := "8000"

build-run: build run

run: stop-and-remove-container
    docker run -dp $PORT:$PORT --name $CONTAINER_NAME -e PORT=$PORT $CONTAINER_NAME

build:
    docker build -t $CONTAINER_NAME .

run-dev: install-python-packages
    #!/bin/zsh

    . $VIRTUAL_ENVIRONMENT/bin/activate
    uvicorn app.main:app --reload

make-api-key: install-python-packages
    #!/bin/zsh

    . $VIRTUAL_ENVIRONMENT/bin/activate
    python scripts/make_api_key.py

copy-api-keys: install-python-packages
    #!/bin/zsh

    . $VIRTUAL_ENVIRONMENT/bin/activate
    python scripts/copy_api_keys.py

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
