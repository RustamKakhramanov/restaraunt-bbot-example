FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /usr/src/chatgpt-manager

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /usr/src/chatgpt-manager/
WORKDIR /usr/src/chatgpt-manager/src/

ENTRYPOINT python3 bot/main.py

