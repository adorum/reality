FROM python:3.7-slim-stretch

RUN mkdir /code
WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY reality_worker ./code
