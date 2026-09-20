import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name='cli-helper-92', log_file='app.log'):
    """
    Dynamic log rotator that breathes with the process lifecycle.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # File handler with 1MB cap and 3 backup files
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=1*1024*1024, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        
        # Stream handler for console visibility
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger

# Quick access factory instance
helper_logger = get_logger()