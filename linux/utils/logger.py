import logging
import os

def setup_logger(name="shellixa", log_file="shellixa.log", level=logging.INFO):
    """Function setup as many loggers as you want"""
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Default logger
if not os.path.exists("logs"):
    os.makedirs("logs")
logger = setup_logger(log_file="logs/shellixa.log")
