FROM jupyter/minimal-notebook

COPY requirements.txt .

USER root
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN pip install -r /tmp/requirements.txt
