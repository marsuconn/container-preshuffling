FROM python:3.10.7
USER root

# Install gcsfuse
ENV GCSFUSE_VERSION=1.2.0

RUN apt-get update -y && \
    apt-get install -y curl && \
    curl -LJO "https://github.com/GoogleCloudPlatform/gcsfuse/releases/download/v${GCSFUSE_VERSION}/gcsfuse_${GCSFUSE_VERSION}_amd64.deb" && \
    apt-get -y install fuse && \
    apt-get clean && \
    dpkg -i "gcsfuse_${GCSFUSE_VERSION}_amd64.deb"

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* 
RUN mkdir bucketdata

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

# EXPOSE 5000

ENV PYTHONUNBUFFERED True
CMD exec gunicorn -c gunicorn.conf.py --worker-class=gevent --worker-connections=1000 --timeout 0 main:app

# newrelic
RUN pip install --no-cache-dir newrelic
RUN mkdir -p /app/newrelic/logs
ADD ./libs/newrelic.ini /app/newrelic/newrelic.ini
ENV NEW_RELIC_CONFIG_FILE=/app/newrelic/newrelic.ini
# ENV NEW_RELIC_ENVIRONMENT=dev
# ENV APP_NAME_PREFIX=ocean-terminal
# ENV NEW_RELIC_APP_NAME="${APP_NAME_PREFIX} ${FLASK_PROFILE}"
ENTRYPOINT ["newrelic-admin", "run-program"]
