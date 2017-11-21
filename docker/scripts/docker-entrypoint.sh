#!/usr/bin/env bash

# populate properties config files from template
/usr/bin/env python /opt/kafka-connect-source/populate-config-files.py

# start kafka-connect-s3
connect-standalone /etc/kafka-connect-source/connect-standalone.properties \
    /etc/kafka-connect-source/connect-jdbc-source.properties