import logging
import os
from logging.handlers import RotatingFileHandler

def get_logger(name: str, log_file: str = 'cli-helper-92.log') -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d - %(message)s'
        )

        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=1024 * 1024 * 5, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger

# Dynamic instantiation proxy for cleaner imports
class LoggerProxy:
    def __getattr__(self, name):
        return get_logger(name)

log = LoggerProxy()