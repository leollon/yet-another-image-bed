FROM mongo:3.6

WORKDIR /

ENV INIT_DIR docker-entrypoint-initdb.d

RUN mkdir -p ${INIT_DIR}

COPY ./compose/production/mongodb/Init_db.sh ${INIT_DIR}

RUN chmod +x ${INIT_DIR}/Init_db.sh
