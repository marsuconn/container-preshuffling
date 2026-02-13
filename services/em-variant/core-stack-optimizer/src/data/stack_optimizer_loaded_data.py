import os
import pickle
import time

import pandas as pd
from gevent.lock import RLock

from src.util.config_loader import Config
import logging

REENTRANT_LOCK = RLock()


class StackOptimizerLoadedData:
    __final_file_name__ = ""
    __data_load_time__ = None

    __prefetched_data__ = {
        "df_curr_mmsi": {"data": pd.DataFrame()},
        "df_prev_mmsi": {"data": pd.DataFrame()},
        "df_curr": {"data": pd.DataFrame()},
        "df_prev": {"data": pd.DataFrame()},
        "df_presaved_terminal": {"data": pd.DataFrame()},
        "mmsi_imo_map": {"data": None},
        "imo_mmsi_map": {"data":None}
    }

    @staticmethod
    def read_files_if_required():
        with REENTRANT_LOCK:
            if StackOptimizerLoadedData.__reload_required():
                StackOptimizerLoadedData.__populate_data_frames()

    @staticmethod
    def __reload_required():
        try:
            if StackOptimizerLoadedData.__data_load_time__ is None:
                return True

            current_modification_time = os.path.getmtime(StackOptimizerLoadedData.__final_file_name__)
            if StackOptimizerLoadedData.__data_load_time__ < current_modification_time:
                return True
            return False
        except:
            return False

    @staticmethod
    def find(name):
        return StackOptimizerLoadedData.__prefetched_data__[name]["data"]

    @staticmethod
    def __populate_data_frames():
        try:
            temporary_data_holder = StackOptimizerLoadedData.__load_data_from_files__()

            final_file_name = StackOptimizerLoadedData.__full_path_general__('filepath_data_completion')
            data_load_time = os.path.getmtime(final_file_name)

            for key, value in temporary_data_holder.items():
                data_item = StackOptimizerLoadedData.__prefetched_data__[key]
                data_item["data"] = value["data"]
                if "file_type" in value:
                    data_item["file_type"] = value["file_type"]

            StackOptimizerLoadedData.__verify_data_sanity__()

            StackOptimizerLoadedData.__final_file_name__ = final_file_name
            StackOptimizerLoadedData.__data_load_time__ = data_load_time

            logging.debug(f"Terminal data loaded with completion file timestamp: {time.ctime(StackOptimizerLoadedData.__data_load_time__)}")
        except Exception as exc:
            logging.error('read_files() : Got exception {}'.format(exc))

    @staticmethod
    def __verify_data_sanity__():
        for key, item in StackOptimizerLoadedData.__prefetched_data__.items():
            if "file_type" not in item:
                raise Exception(f"Ensure file_type is populated for {key}")
            if not item["file_type"] == "derived" and "path" not in item:
                raise Exception(f"Ensure path is populated for {key}")
            if "data" not in item or item["data"] is None:
                raise Exception(f"Data is not populated for {key}")

    @staticmethod
    def __load_data_from_files__():
        StackOptimizerLoadedData.__populate_paths__()
        temporary_data_holder = {}
        for key, data_item in StackOptimizerLoadedData.__prefetched_data__.items():
            if "file_type" in data_item:
                file_type = data_item["file_type"]
                file_path = str(data_item["path"])
                data = None
                if file_type == "parquet":
                    data = pd.read_parquet(file_path)
                elif file_type == "csv":
                    data = pd.read_csv(file_path)
                elif file_type == "pickle":
                    with open(file_path, 'rb') as pickle_file:
                        data = pickle.load(pickle_file)

                temporary_data_holder[key] = {
                    "data": data
                }

        temporary_data_holder["mmsi_imo_map"] = {
            "data": temporary_data_holder["df_curr_mmsi"]["data"][['mmsi', 'imo']].set_index('mmsi').to_dict()['imo'],
            "file_type": "derived"
        }

        temporary_data_holder["imo_mmsi_map"] = {
            "data": temporary_data_holder["df_curr_mmsi"]["data"][['mmsi','imo','ARRIVAL_DATE']].loc[temporary_data_holder["df_curr_mmsi"]["data"].groupby('imo')['ARRIVAL_DATE'].idxmax(), ['imo', 'mmsi']].set_index('imo')['mmsi'].to_dict(),
            "file_type": "derived"
        }

        return temporary_data_holder

    @staticmethod
    def __populate_paths__():
        fp_df_curr_mmsi = StackOptimizerLoadedData.__full_path_general__('filepath_df_mmsi')
        StackOptimizerLoadedData.__add_path__("df_curr_mmsi", fp_df_curr_mmsi)

        fp_df_prev_mmsi = StackOptimizerLoadedData.__full_path_general__('filepath_prev_df_mmsi')
        StackOptimizerLoadedData.__add_path__("df_prev_mmsi", fp_df_prev_mmsi)

        fp_df_curr = StackOptimizerLoadedData.__full_path_general__('filepath_df')
        StackOptimizerLoadedData.__add_path__("df_curr", fp_df_curr)

        fp_df_prev = StackOptimizerLoadedData.__full_path_general__('filepath_prev_df')
        StackOptimizerLoadedData.__add_path__("df_prev", fp_df_prev)

        fp_presaved_terminal = StackOptimizerLoadedData.__full_path_general__('filepath_presaved_terminal')
        StackOptimizerLoadedData.__add_path__("df_presaved_terminal", fp_presaved_terminal,"csv")

    @staticmethod
    def __full_path_general__(file_name):
        folder_path = Config.value("root_folder") + Config.value('support_folder')

        support_folder_path_general = folder_path + Config.value('folderpath')['general']
        return support_folder_path_general + Config.value('filepath')[file_name]

    @staticmethod
    def __add_path__(key, path, file_type="parquet"):
        data_item = StackOptimizerLoadedData.__prefetched_data__[key]
        data_item["path"] = path
        data_item["file_type"] = file_type
