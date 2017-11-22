import os
import yaml


class Utils:
    @staticmethod
    def get_config_file(filename="config.yml", path=""):
        config_file_path = os.path.expanduser(path)
        print("Loading configFile: {}".format(config_file_path + filename))
        with open(config_file_path + filename, 'r') as ymlfile:
            cfg = yaml.safe_load(ymlfile)
        return cfg

    def get_configuration(self, env_variable_name, config_key_list):
        cfg = self.get_config_file()
        try:
            configuration = os.environ[env_variable_name]
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
