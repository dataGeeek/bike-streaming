import sys
from os import environ
from satori_ingestion.helper.database_manager import SimpleTrainingDatabase
from satori_ingestion.helper.parseconfig import GetConfig
from satori_ingestion.helper.utils import Utils

CFG = GetConfig.get_config_file()


class SubscriptionObserver(object):
    def __init__(self, channel):
        self._channel = channel
        self.__db_path = Utils().get_configuration('SATORI_DB_PATH', ['ingestor', 'dbpath'])
        self.__db = SimpleTrainingDatabase(self.__db_path)
        self.__data_buffer = {}
        for key in self.__db.TrainingDataModel().getColumnNamesDict():
            self.__data_buffer[key] = 0

    def on_enter_subscribed(self):
        print('Subscribed to the channel: ' + self._channel)

    @staticmethod
    def on_enter_failed(reason):
        print('Subscription failed, reason:', reason)
        sys.exit(1)

    def on_subscription_data(self, data):
        for message in data['messages']:
            for key in message:
                self.__data_buffer[key] = message[key]
            self.write_to_db()

    def write_to_db(self):
        db_object = self.__db.TrainingDataModel()
        print(self.__data_buffer)
        for key in self.__data_buffer.keys():
            setattr(db_object, key, self.__data_buffer[key])
        self.__db.write_to_db(db_object)

