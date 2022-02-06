FROM python:3.10.2-slim AS build

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean \
    && apt-get autoremove

ENV APP_CODE=/usr/src/app
RUN mkdir $APP_CODE
WORKDIR $APP_CODE

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY Pipfile Pipfile.lock $APP_CODE/
RUN python -m pip install --upgrade pip && pip install pipenv && pipenv install --system

COPY . $APP_CODE/

FROM build AS test
CMD flake8 -v --ignore=E501 --output-file=./docs/Flake8/flake8.log
CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
