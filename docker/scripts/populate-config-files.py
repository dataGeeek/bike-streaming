#!/usr/bin/env python
from os import environ

def fill_template_from_environment(template_filename, target_filename):
    with open(template_filename, 'r') as template_file, open(target_filename, 'w') as target_file:
        try:
            template = template_file.read()
            filled_template = template.format(**environ)
            target_file.write(filled_template)
        except KeyError:
            print("Please specify all required environment variables!")

fill_template_from_environment('/etc/kafka-connect-source/connect-standalone.properties.template',
                               '/etc/kafka-connect-source/connect-standalone.properties')
fill_template_from_environment('/etc/kafka-connect-source/connect-jdbc-source.properties.template',
                               '/etc/kafka-connect-source/connect-jdbc-source.properties')