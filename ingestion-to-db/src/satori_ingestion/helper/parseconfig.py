import os
import yaml


class GetConfig:
    @staticmethod
    def get_config_file(filename="config.yml", path=""):
        config_file_path = os.path.expanduser(path)
        print("Loading configFile: {}".format(config_file_path + filename))
        with open(config_file_path + filename, 'r') as ymlfile:
            cfg = yaml.safe_load(ymlfile)
        return cfg
