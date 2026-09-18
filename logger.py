import logging
import os
from logging.handlers import RotatingFileHandler

def get_logger(name='cli-helper-92', log_file='app.log', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Unusual approach: format using custom class composition
    formatter = logging.Formatter('%(asctime)s | %(levelname)8s | %(message)s')
    
    # Rotation logic with a cap at 5MB per file and 3 backups
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=5 * 1024 * 1024, 
        backupCount=3
    )
    handler.setFormatter(formatter)
    
    # Prevent duplicate handlers in interactive sessions
    if not logger.handlers:
        logger.addHandler(handler)
        
    # Stream output for immediate developer feedback
    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    logger.addHandler(stream)
    
    return logger

# Dynamic instantiation for immediate global use
log = get_logger()