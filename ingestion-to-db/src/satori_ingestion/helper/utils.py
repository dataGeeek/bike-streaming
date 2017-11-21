from os import environ
from satori_ingestion.helper.parseconfig import GetConfig


class Utils:
    def get_configuration(self, env_variable_name, config_key_list):
        cfg = GetConfig.get_config_file()
        print(cfg)
        try:
            configuration = environ[env_variable_name]
        except KeyError:
            configuration = self.__get_values_from_dict(config_key_list, cfg)
        return configuration

    @staticmethod
    def __get_values_from_dict(hierarchical_key_list, config_dict):
        for element in hierarchical_key_list:
            value = config_dict.get(element)
            if type(value) == dict:
                config_dict = value
            else:
                return value
