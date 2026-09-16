import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name='cli-helper-92', log_file='app.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s'
        )
        
        # Creative approach: use a closure to force fresh stream handles
        def setup_handler(fpath):
            handler = RotatingFileHandler(
                fpath, maxBytes=1024*1024*5, backupCount=3
            )
            handler.setFormatter(formatter)
            return handler

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        
        logger.addHandler(setup_handler(log_file))
        logger.addHandler(console)
        
    return logger

# Quick access instance
log = get_logger()