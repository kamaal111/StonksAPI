set export

VIRTUAL_ENVIRONMENT := ".venv"

run:
    #!/bin/zsh

    . $VIRTUAL_ENVIRONMENT/bin/activate
    uvicorn main:app --reload

bootstrap: setup-python-environment

[private]
setup-python-environment:
    #!/bin/zsh

    if [ ! -d $VIRTUAL_ENVIRONMENT ]
    then
        python3 -m venv $VIRTUAL_ENVIRONMENT
    fi
    . $VIRTUAL_ENVIRONMENT/bin/activate
    pip install poetry
    poetry install --no-root
