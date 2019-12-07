#!/bin/bash

mongo -u "${MONGO_INITDB_ROOT_USERNAME}" -p "${MONGO_INITDB_ROOT_PASSWORD}" localhost:27017/admin << EOJS
use ${MONGO_INITDB_DATABASE};
db.createUser({user: "${MONGO_USER}", pwd: "${MONGO_USER_PASSWORD}", roles: [{role: "readWrite", db: "${MONGO_INITDB_DATABASE}"}]});
EOJS

