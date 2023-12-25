set export

VIRTUAL_ENVIRONMENT := ".venv"

run:
    #!/bin/zsh

    just install-python-packages
    . $VIRTUAL_ENVIRONMENT/bin/activate
    uvicorn app.main:app --reload

bootstrap: setup-python-environment

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
