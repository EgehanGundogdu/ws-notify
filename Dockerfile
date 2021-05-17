FROM python:3-alpine

LABEL MAINTAINER="Egehan Gündoğdu <egehn.gundogdu@gmail.com>"

ENV PYTHONBUFFERED=1

ENV PYTHONDONTWRITEBYTECODE=1

RUN apk add --update --no-cache postgresql-client jpeg-dev \
    && apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev libffi-dev cargo rust openssl-dev

COPY ./requirements.txt /requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN apk del .tmp-build-deps 

WORKDIR /usr/src/app

COPY ./app .

RUN mkdir -p /vol/web/media && mkdir -p /vol/web/static && chmod -R 755 /vol/web
