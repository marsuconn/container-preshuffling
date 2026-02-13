FROM python:3.10.7
USER root
RUN apt-get update
RUN apt-get install --yes --no-install-recommends ca-certificates curl gpg 
RUN echo "deb http://packages.cloud.google.com/apt gcsfuse-stretch main" | tee /etc/apt/sources.list.d/gcsfuse.list 
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - 
RUN apt-get update 
RUN apt-get install --yes gcsfuse 
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
