#!/bin/bash
set -e

RED='\033[0;31m'
NOCOLOR='\033[0m'

if [ ${UID} != 0 ]
then
    echo "run this script as root."
    exit 1
fi

OS_ID=$(grep -i "^id=.*" /etc/os-release | cut -d '=' -f2)
if [ "${OS_ID}" != "ubuntu" ] && [ "${OS_ID}" != "debian" ]
then
    echo -e "${RED}Only run this script on debian-like OS.${NOCOLOR}"
    exit 1
fi

apt-get update && apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common -yq

curl -fsSL "https://download.docker.com/linux/${OS_ID}/gpg" | apt-key add -

add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/${OS_ID} \
   $(lsb_release -cs) \
   stable" -y

apt-get update && apt-get install -qq docker-ce

curl -fsSL "https://github.com/docker/compose/releases/download/1.25.0/\
docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

chmod +x /usr/local/bin/docker-compose ./up ./down

./up --build -d

docker-compose -f docker-compose.yml ps
