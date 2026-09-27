import logging
from logging.handlers import RotatingFileHandler
import os

class CreativeLogger:
    def __init__(self, name='cli-helper-92', log_file='app.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(process)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # console sink
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)

        # rotating file sink: 1MB per file, keep 3 backups
        rotator = RotatingFileHandler(
            log_file, 
            maxBytes=1024*1024, 
            backupCount=3
        )
        rotator.setFormatter(formatter)
        self.logger.addHandler(rotator)

    def get_logger(self):
        return self.logger

# global singleton instance
_instance = CreativeLogger()
logger = _instance.get_logger()

def get_log_hook():
    return logger