#!/bin/bash

if [ $UID != 0 ]
then
    echo "run this script as root."
    exit 1
fi

OS_ID=$(grep -i "^id=.*" /etc/os-release | cut -d '=' -f 2)
apt-get update && apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common -yq

curl -fsSL "https://download.docker.com/linux/${OS_ID}/gpg" | apt-key add -

add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/$OS_ID \
   $(lsb_release -cs) \
   stable" -y

apt update && apt install docker-ce -yq

curl -L "https://github.com/docker/compose/releases/download/1.22.0/\
docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

chmod +x /usr/local/bin/docker-compose ./up ./down

./up --build -d

docker container exec -i "$(docker-compose -f docker-compose.yml ps | grep 'mongo_1' | awk '{print $1}')" mongo < compose/production/mongodb/createUser.js

docker-compose -f docker-compose.yml ps
