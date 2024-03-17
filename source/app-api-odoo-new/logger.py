import logging
import datetime
import os
import sys

log_directory = '/var/log/fastapi'
os.makedirs(log_directory, exist_ok=True)

### Log Custom
func_log = logging.getLogger("custom.fastapi.log")
func_log.setLevel(logging.INFO)
func_log.propagate = False
log_file_func = log_directory+'/log_custom_{date}.log'
log_file_func = log_file_func.format(date=datetime.date.today())
func_handler = logging.FileHandler(log_file_func)
func_handler.setFormatter(logging.Formatter("[%(asctime)s] - [%(name)s] - [%(levelname)s] - [%(message)s]"))
func_log.addHandler(func_handler)

### Log std
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s] - [%(name)s] - [%(levelname)s] - [%(message)s]")
log_file_std = log_directory+'/log_uvicorn_{date}.log'
log_file_std = log_file_std.format(date=datetime.date.today())
file_handler = logging.FileHandler(log_file_std)
file_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(file_handler)
logger.propagate = False