import logging
import os
import sys

def setup_logger(name="shellixa", log_file="logs/shellixa.log", level=logging.INFO):
    """Set up logger with both file and console handlers."""
    # Ensure directory exists
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    # File Handler
    file_handler = logging.FileHandler(log_file)        
    file_handler.setFormatter(formatter)

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers if setup is called multiple times
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Initialize default logger
logger = setup_logger()
logger.info("Shellixa Logging System Initialized")
