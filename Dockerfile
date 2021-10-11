FROM python:3.9.7-alpine3.14

ARG HOST
ARG DB
ARG USER
ARG PASSWORD
ARG AUTHENTICATION_SOURCE

ENV APP_SETTINGS "Prod"
ENV APP_PATH "/usr/src/application"
ENV LOGGER_NAME "logger"
ENV URL_WEBSITE  "http://172.17.0.252/index2.php?c=12"

ENV HOST $HOST
ENV DB $DB
ENV USER $USER
ENV PASSWORD $PASSWORD
ENV AUTHENTICATION_SOURCE $AUTHENTICATION_SOURCE

WORKDIR ${APP_PATH}

RUN pip install --upgrade pip

COPY ./ ${APP_PATH}

RUN apk add --update --no-cache g++ gcc libxslt-dev

RUN pip install --no-cache-dir -r ${APP_PATH}/requirements/production.txt

RUN chmod +x ${APP_PATH}/run_app.sh

RUN echo "*/30   *   *   *   *   ${APP_PATH}/run_app.sh" > /etc/crontabs/root

CMD sh ${APP_PATH}/run_app.sh ; crond -f -l 2
