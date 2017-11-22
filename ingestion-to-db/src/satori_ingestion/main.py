#!/usr/bin/env python

import logging
from satori.rtm.client import make_client, SubscriptionMode
from satori_ingestion.subscription_observer import SubscriptionObserver
from satori_ingestion.helper.utils import Utils
from time import sleep

logging.basicConfig(level=logging.WARNING)
CFG = Utils.get_config_file()
channel = Utils().get_configuration('SATORI_CHANNEL', ['ingestor', 'channel'])
endpoint = Utils().get_configuration('SATORI_ENDPOINT', ['ingestor', 'endpoint'])
appkey = CFG['ingestor']['apikey']


class SatoriIngestion:
    def __init__(self):
        self.__CFG = Utils.get_config_file()
        self.__channel = Utils().get_configuration('SATORI_CHANNEL', ['ingestor', 'channel'])
        self.__endpoint = Utils().get_configuration('SATORI_ENDPOINT', ['ingestor', 'endpoint'])
        self.__appkey = CFG['ingestor']['apikey']

    def main(self):
        with make_client(
                endpoint=self.__endpoint, appkey=self.__appkey,
                auth_delegate=None) as client:
            subscription_observer = SubscriptionObserver(channel=self.__channel)
            client.subscribe(
                channel,
                SubscriptionMode.SIMPLE,
                subscription_observer)

            while True:
                sleep(1)


if __name__ == '__main__':
    SatoriIngestion().main()
