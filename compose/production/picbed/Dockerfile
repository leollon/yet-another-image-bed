# 使用python:3.7-alpine作为父镜像
FROM python:3.7-alpine

LABEL Name=picbed Version=1.0.0

# 环境变量
ENV PYTHONUNBUFFERED 1
ENV RUN_DIR run
ENV UPLOAD_DIR upload


RUN apk add --no-cache \
        -X http://mirrors.ustc.edu.cn/alpine/v$(cat /etc/issue | tr -d '[a-zA-Z\(\)\ \\\n]')/main/ \
        gcc linux-headers libc-dev \
        python3-dev bash

RUN mkdir /picbed
WORKDIR /picbed

RUN adduser -s /bin/bash -DH picbed
RUN echo 'picbed ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN echo 'picbed:picbed' | chpasswd

# 将代码文件以及相关配置文件添加到/home/picbed中
COPY requirements.txt ./
COPY app ./app
COPY config.py ./config.py
COPY wsgi.py ./
COPY compose/production/picbed/entrypoint /entrypoint

# Install dependencies
RUN pip install -i https://pypi.doubanio.com/simple/ \
        -r requirements.txt && rm -f requirements.txt

RUN mkdir -p ${UPLOAD_DIR}

RUN chown -R picbed:picbed /picbed /entrypoint
RUN chmod -R 755 /picbed /entrypoint

# 使用picbed用户执行 `RUN`, `CMD` and `ENTRYPOINT`
USER picbed:picbed
