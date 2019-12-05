# 使用python:3.7-alpine作为父镜像
FROM python:3.7-alpine

LABEL Name=picbed Version=1.0.0

WORKDIR /

# 环境变量
ENV PYTHONUNBUFFERED 1
ENV PIDFILE /picbed/run/picbed-manager.pid

RUN apk add --no-cache \
        -X http://mirrors.ustc.edu.cn/alpine/v$(cat /etc/issue | tr -d '[a-zA-Z\(\)\ \\\n]')/main/ \
        gcc linux-headers libc-dev \
        python3-dev bash

RUN adduser -s /bin/bash -DH picbed
RUN echo 'picbed ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN echo 'picbed:picbed' | chpasswd
RUN mkdir -p ${UPLOAD_DIR} picbed /picbed/${RUN_DIR}

# 将代码文件以及相关配置文件添加到/home/picbed中
COPY requirements.txt ./
# Install dependencies
RUN pip install -i https://pypi.doubanio.com/simple/ -r requirements.txt && \
    rm -f requirements.txt

COPY compose/production/picbed/entrypoint /entrypoint
COPY compose/production/picbed/uwsgi.ini /uwsgi.ini
ADD ./picbed picbed

RUN chown -R picbed:picbed /picbed /picbed/${RUN_DIR} /entrypoint /uwsgi.ini 
RUN chmod -R 755 /picbed /picbed/${RUN_DIR} /entrypoint /uwsgi.ini

# 使用picbed用户执行 `RUN`, `CMD` and `ENTRYPOINT`
USER picbed:picbed
WORKDIR /picbed

RUN echo -e "uid=picbed\ngid=picbed\nhome=/usr/local/\nchdir=/picbed\npidfile=${PIDFILE}\n" >> \
    /uwsgi.ini
