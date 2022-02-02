FROM python:3.10

RUN python -m pip install --upgrade pip
# set work directory
ENV APP_HOME=/usr/src/app
RUN mkdir $APP_HOME
WORKDIR $APP_HOME
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
COPY Pipfile Pipfile.lock $APP_HOME/
RUN pip install pipenv && pipenv install --system
# copy project
COPY . $APP_HOME/