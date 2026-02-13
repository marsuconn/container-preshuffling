import os
import yaml
import logging

class Config:
    __conf__ = {}

    __file_paths__ = {
        "package": "./core-stack-optimizer/",
        "workers": 5,
        "root_folder": "/bucketdata/",
        "folderpath": "application_support/appointment_scheduling/"
    }

    @staticmethod
    def value(key):
        if not Config.__conf__:
            Config.initialize()
        return Config.__conf__[key]

    @staticmethod
    def initialize():
        flask_profile = os.environ.get('FLASK_PROFILE')
        if flask_profile is None:
            flask_profile = 'local-dev'
        
        if flask_profile in ['dev','qa','perf']:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        config_file_name = f"./config/{flask_profile}.yml"

        Config.initialize_from_file(config_file_name)

    @staticmethod
    def initialize_from_file(file_name):
        if os.path.exists(file_name):
            with open(file_name, mode="r", encoding="UTF-8") as yml_file:
                Config.__conf__ = {**Config.__file_paths__, **yaml.safe_load(yml_file)}
        else:
            Config.__conf__ = Config.__file_paths__
