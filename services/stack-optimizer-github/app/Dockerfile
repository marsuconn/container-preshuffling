FROM openjdk:8-jdk-alpine
ADD build/libs/app-0.0.1-SNAPSHOT.jar opt/stackoptimizer-0.0.1-SNAPSHOT.jar
# JRE fails to load fonts if there are no standard fonts in the image; DejaVu is a good choice,
# see https://github.com/docker-library/openjdk/issues/73#issuecomment-207816707
RUN apk add --update ttf-dejavu && rm -rf /var/cache/apk/*
RUN mkdir -p /usr/local/newrelic/logs
ADD libs/newrelic.jar /usr/local/newrelic/newrelic.jar
ADD libs/newrelic.yml /usr/local/newrelic/newrelic.yml
ENV SPRING_PROFILE="to be overridden from yaml"
WORKDIR /opt/
ENTRYPOINT exec java -Dnewrelic.environment=$SPRING_PROFILE -javaagent:/usr/local/newrelic/newrelic.jar -Dspring.profiles.active=$SPRING_PROFILE -jar stackoptimizer-0.0.1-SNAPSHOT.jar
