FROM python:3

RUN mkdir -p /opt/src/satori_ingestion
ADD satori_ingestion /opt/target/satori_ingestion
COPY config.yml /opt/target
COPY setup.py /opt/target

RUN chmod +x /opt/target/setup.py && cd /opt/target && python setup.py install
RUN chmod +x /opt/target/satori_ingestion/docker/entrypoint.sh

ENTRYPOINT ["/opt/target/satori_ingestion/docker/entrypoint.sh"]