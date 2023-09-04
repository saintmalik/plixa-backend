FROM python:3.11-bullseye

WORKDIR /plixa_backend

COPY Pipfile Pipfile.lock /plixa_backend/

RUN pip install --no-cache-dir pip

RUN pip install --no-cache-dir pipenv

RUN pipenv install --system

COPY . .