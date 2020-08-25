FROM python:3.7
LABEL maintainer="duoduod3369@gmail.com"

ARG DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED 1
WORKDIR /opt/projects/magic_scripts

COPY requirements.txt /opt/projects/magic_scripts/requirements.txt

RUN cp /etc/apt/sources.list /etc/apt/sources.list.back && \
    sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list && \
    sed -i s@/security.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get update && apt-get install -yq vim

ENV REFRESHED_AT 2020-08-25_18:10
RUN pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
