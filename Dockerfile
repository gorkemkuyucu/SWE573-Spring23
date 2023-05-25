FROM python:3.9.16-slim-buster

LABEL maintainer="onceuponatime.com"

ENV PYTHONUNBEFFERED 1

# Install dependencies (like GDAL and GEOS)
RUN apt-get update && apt-get install -y \
    binutils libproj-dev gdal-bin python-gdal python3-gdal \
    libgeos-dev python3-dev netcat postgresql gcc libpq-dev

COPY ./requirements.txt /requirements.txt
COPY ./ ./OnceUponATime

WORKDIR /OnceUponATime
EXPOSE 8000

RUN python -m venv /py \
    && /py/bin/pip install --upgrade pip \
    && /py/bin/pip install -r /requirements.txt \
    && adduser --disabled-password --gecos '' app

ENV PATH="/py/bin:$PATH"
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

USER app
