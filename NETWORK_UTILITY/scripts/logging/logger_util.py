import logging
import os
from logging.handlers import RotatingFileHandler

from scripts.constants.app_configuration import app_config as config

_log_file_name__ = config["LOG"]["file_name"]
__log_path__ = config["LOG"]["base_path"]
__log_level__ = config["LOG"]["log_level"]
__handler_type__ = config["LOG"]["handlers"]
__max_bytes__ = config["LOG"]["max_bytes"]
__backup_count__ = config["LOG"]["back_up_count"]
complete_log_path = os.path.join(__log_path__, _log_file_name__)
if not os.path.isdir(__log_path__):
    os.makedirs(__log_path__)


def get_logger(log_file_name=complete_log_path, log_level=__log_level__,
               time_format="%Y-%m-%d %H:%M:%S",
               handler_type=__handler_type__, max_bytes=__max_bytes__,
               backup_count=__backup_count__):
    """
     Creates a rotating log
     """
    log_file = os.path.join(log_file_name + '.log')
    __logger__ = logging.getLogger(log_file_name)
    __logger__.setLevel(log_level.strip().upper())
    debug_formatter = '%(asctime)s - %(levelname)-6s - [%(threadName)5s:%(filename)5s:%(funcName)5s():''%(lineno)s] - %(message)s'
    formatter_string = '%(asctime)s - %(levelname)-6s- - %(message)s'

    if log_level.strip().upper() == log_level:
        formatter_string = debug_formatter

    formatter = logging.Formatter(formatter_string, time_format)

    # if str(handler_type).lower() == "console_handler":
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    if __logger__.hasHandlers():
        __logger__.handlers.clear()
    # __logger__.addHandler(console_handler)

    if str(handler_type).lower() == "rotating_file_handler":
        # Rotating File Handler
        handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        handler.setFormatter(formatter)
        if __logger__.hasHandlers():
            __logger__.handlers.clear()
        __logger__.addHandler(handler)

    else:
        # File Handler
        hdlr_service = logging.FileHandler(log_file)
        hdlr_service.setFormatter(formatter)
        if __logger__.hasHandlers():
            __logger__.handlers.clear()
        __logger__.addHandler(hdlr_service)

    return __logger__


logger = get_logger()
