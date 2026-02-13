import os
import yaml
import logging

class Config:
    __conf__ = {}

    __file_paths__ = {
        "package": "./ocean-terminal/",
        "workers": 5,
        "root_folder": "/bucketdata/",
        "support_folder": "api_support/ocean/terminal/dependencies/",
        "folderpath": {
            "general": "general/"
        },
        "filepath": {
            "filepath_df_mmsi": "d1_mmsi.parquet",
            "filepath_prev_df_mmsi": "prev_data_mmsi.parquet",
            "filepath_df": "d1.parquet",
            "filepath_prev_df": "prev_data.parquet",
            "filepath_ais": "ais_ml_data_v4_29112021.csv",
            "filepath_imo": "mmsi_filter_21k",
            "filepath_data_completion": "OCEAN-TERMINAL-COMPLETE.csv",
            "filepath_presaved_terminal":"df_presaved_terminal.csv"
        }
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
            flask_profile = 'dev'
        
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
