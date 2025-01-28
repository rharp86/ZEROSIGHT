### utils/logger.py
import logging
import os
from datetime import datetime

def setup_logger(target: str, log_level=logging.INFO) -> logging.Logger:
    log_dir = os.path.join("logs", target)
    os.makedirs(log_dir, exist_ok=True)

    run_number = 1
    while os.path.exists(os.path.join(log_dir, f"Run{run_number}")):
        run_number += 1
    
    run_dir = os.path.join(log_dir, f"Run{run_number}")
    os.makedirs(run_dir, exist_ok=True)
    
    log_file = os.path.join(run_dir, "execution.log")
    
    logger = logging.getLogger(target)
    logger.setLevel(log_level)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger