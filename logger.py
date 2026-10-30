import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name='cli-helper-92', log_file='app.log', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Creative spin: max 5MB files, keep 3 backups
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=5*1024*1024, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Fallback to console if running in dev environment
        if os.getenv('DEV_MODE') == 'true':
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            
    return logger

# Instantiate for quick imports
logger = setup_logger()