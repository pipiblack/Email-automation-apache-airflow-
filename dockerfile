FROM apache/airflow:latest

USER root

RUN apt-get update && \
    apt-get -y install git && \
    apt-get clean

USER airflow

# install custom packages

COPY requirements.txt /tmp/requirements.txt

# RUN pip install -r requirements.txt