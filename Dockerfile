FROM python:3.10

#
WORKDIR /code

#
COPY ./poetry.lock /code/poetry.lock
COPY ./pyproject.toml /code/pyproject.toml

RUN pip install --no-cache-dir --upgrade pip
RUN pip install -U pip poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

COPY ./src /code/src