FROM java:8

ENV CONNECT_VERSION 3.3.0-1
ENV KAFKA_VERSION 0.11.0.0-1

# install confluent platform + s3 plugin
RUN wget -qO - http://packages.confluent.io/deb/3.3/archive.key | apt-key add - \
 && /bin/bash -c "echo 'deb [arch=amd64] http://packages.confluent.io/deb/3.3 stable main' >> /etc/apt/sources.list" \
 && apt-get update \
 && apt-get install -y \
 confluent-platform-oss-2.11=$CONNECT_VERSION \
 confluent-kafka-connect-s3=$CONNECT_VERSION \
 confluent-camus=$CONNECT_VERSION \
 confluent-common=$CONNECT_VERSION \
 confluent-kafka-2.11=$KAFKA_VERSION \
 confluent-kafka-connect-elasticsearch=$CONNECT_VERSION \
 confluent-kafka-connect-hdfs=$CONNECT_VERSION \
 confluent-kafka-connect-jdbc=$CONNECT_VERSION \
 confluent-kafka-connect-storage-common=$CONNECT_VERSION \
 confluent-rest-utils=$CONNECT_VERSION \
 confluent-kafka-rest confluent-schema-registry=$CONNECT_VERSION

# copy config files
RUN mkdir -p /etc/kafka-connect-source/

COPY config/connect-standalone.properties.template /etc/kafka-connect-source/
COPY config/connect-jdbc-source.properties.template /etc/kafka-connect-source/

RUN mkdir -p /opt/kafka-connect-source/
# configure entrypoint
COPY scripts/populate-config-files.py /opt/kafka-connect-source/
RUN chmod +x /opt/kafka-connect-source/populate-config-files.py

COPY scripts/docker-entrypoint.sh /opt/kafka-connect-source/
RUN chmod +x /opt/kafka-connect-source/docker-entrypoint.sh

ENTRYPOINT ["/opt/kafka-connect-source/docker-entrypoint.sh"]