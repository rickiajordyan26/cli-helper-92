import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name: str, log_file: str = 'app.log', max_bytes: int = 1048576, backup_count: int = 3):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(name)s | %(message)s')
    
    # rotating file handler to keep things tidy
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=max_bytes, 
        backupCount=backup_count
    )
    file_handler.setFormatter(formatter)
    
    # console handler for immediate visibility
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

if __name__ == '__main__':
    log = setup_logger('cli-helper-92')
    log.info('logger initialized and ready')