import os
from .logger import Logger
from .write_data_cols_m import write_data_cols

PATH = os.path.abspath(os.path.dirname(__file__))
logger_obj = Logger(f'{PATH}/logs')
def logger():
    return logger_obj.get_logger()