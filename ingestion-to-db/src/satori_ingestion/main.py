#!/usr/bin/env python

import logging
from satori.rtm.client import make_client, SubscriptionMode
from satori_ingestion.subscription_observer import SubscriptionObserver
from satori_ingestion.helper.utils import Utils

logging.basicConfig(level=logging.WARNING)
CFG = Utils.get_config_file()
channel = Utils().get_configuration('SATORI_CHANNEL', ['ingestor', 'channel'])
endpoint = Utils().get_configuration('SATORI_ENDPOINT', ['ingestor', 'endpoint'])
appkey = CFG['ingestor']['apikey']


def main():

    with make_client(
            endpoint=endpoint, appkey=appkey,
            auth_delegate=None) as client:
        subscription_observer = SubscriptionObserver(channel=channel)
        client.subscribe(
            channel,
            SubscriptionMode.SIMPLE,
            subscription_observer)

        n = 0
        while True:
            n = n + 1


if __name__ == '__main__':
    main()
