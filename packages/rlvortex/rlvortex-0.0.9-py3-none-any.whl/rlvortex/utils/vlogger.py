import os
import enum
import logging
import json
from datetime import datetime, timezone


class LogType(enum.Enum):
    Vanish = 1
    Screen = 2
    File = 3


class VLogger:
    def __init__(self, log_type: LogType, log_path: os.path or None = None) -> None:
        self.start_time_str = datetime.now(timezone.utc).astimezone().strftime("%H:%M:%S-%d_%m_%y")
        self.log_type = log_type
        self.log_path = log_path
        self.__setup_logger_config()

    def __setup_logger_config(self):
        if self.log_type == LogType.File:
            logging.basicConfig(
                filename=self.log_path,
                filemode="a",
                format="%(asctime)s-%(levelname)s \n%(message)s",
                level=os.environ.get("LOGLEVEL", "INFO"),
            )
        elif self.log_type == LogType.Screen:
            logging.basicConfig(
                format="%(asctime)s-%(levelname)s \n%(message)s", level=os.environ.get("LOGLEVEL", "INFO"),
            )

    def info_dict(self, dict_info: dict):
        if self.log_type == LogType.Vanish:
            return
        logging.info(json.dumps(dict_info, sort_keys=False, indent=4))

    def info(self, msg: str):
        if self.log_type == LogType.Vanish:
            return
        logging.info(msg)

    def debug(self, msg: str):
        if self.log_type == LogType.Vanish:
            return
        logging.debug(msg)
