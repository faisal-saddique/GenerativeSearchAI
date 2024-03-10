# logger_setup.py

import logging
import os
import datetime

def setup_logging():
    
    # Determine the root directory of the project
    root_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(root_dir, "__log_files__")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    time_now = str(datetime.datetime.now()).replace(":", "_").replace(" ", "_")
    log_file_name = os.path.join(log_dir, f"logs_{time_now}.log")

    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create file handler for logging to a file
    file_handler = logging.FileHandler(log_file_name)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Create console handler for logging to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Optional: Prevent logging from propagating to the root logger
    logger.propagate = False