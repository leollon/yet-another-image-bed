# 使用python:3.7-alpine作为父镜像
FROM python:3.7-alpine

LABEL Name=imgbed Version=1.0.0

# 环境变量
ENV PYTHONUNBUFFERED 1
ENV LOG_DIR log/uwsgi
ENV DEPLOY_DIR deploy
ENV LOGFILE log/uwsgi/uwsgi.log
ENV PIDFILE deploy/imgbed-manager.pid
ENV IMG_DIR upload

RUN apk add --no-cache \
        -X http://mirrors.ustc.edu.cn/alpine/v$(cat /etc/issue | egrep [0-9\.] | tr -d [a-zA-Z\ ])/main/ \
        gcc linux-headers libc-dev \
        python3-dev libffi-dev openssl-dev \
        bash

RUN rm -rf \
        /usr/local/share/doc \
        /usr/local/share/man \
    && find /usr/local -name '*.a' -delete


RUN mkdir /home/imgbed
WORKDIR /home/imgbed

RUN adduser -D -s /bin/bash -h /home/imgbed imgbed
RUN echo 'imgbed ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN echo 'imgbed:imgbed' | chpasswd

# 将代码文件以及相关配置文件添加到/home/imgbed中
COPY requirements.txt ./
COPY app ./app
COPY config.py ./config.py
COPY wsgi.py ./
COPY compose/production/picbed/uwsgi.ini ./uwsgi.ini

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && rm -f requirements.txt

RUN mkdir -p $LOG_DIR $DEPLOY_DIR $IMG_DIR
RUN touch $PIDFILE $LOGFILE

RUN chown -R imgbed:imgbed ./
RUN chmod -R 755 ./

# 使用imgbed用户执行 `RUN`, `CMD` and `ENTRYPOINT`
USER imgbed

RUN bash -c "echo -e \"uid=imgbed\ngid=imgbed\nhome=/usr/local/\nchdir=./\npidfile=$PIDFILE\nlogto=$LOGFILE\" >> \
    ./uwsgi.ini"
