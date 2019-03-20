
# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.

# 使用python:3.6作为父镜像
FROM python:3.6

LABEL Name=imgbed Version=1.0.0

# 环境变量
ENV PYTHONUNBUFFERED 1
ENV LOG_DIR log/uwsgi
ENV DEPLOY_DIR deploy
ENV LOGFILE log/uwsgi/uwsgi.log
ENV PIDFILE deploy/imgbed-manager.pid
ENV IMG_DIR upload

RUN mkdir /home/imgbed
WORKDIR /home/imgbed

RUN useradd -s /bin/bash -d /home/imgbed imgbed
RUN usermod -aG imgbed imgbed
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
RUN chown -R imgbed:imgbed ./
RUN chmod -R 755 ./

# 使用imgbed用户执行 `RUN`, `CMD` and `ENTRYPOINT`
USER imgbed

RUN mkdir -p $LOG_DIR $DEPLOY_DIR $IMG_DIR
RUN touch $PIDFILE $LOGFILE

RUN bash -c "echo -e \"uid=imgbed\ngid=imgbed\nhome=/usr/local/\nchdir=./\npidfile=$PIDFILE\nlogto=$LOGFILE\" >> \
    ./uwsgi.ini"
