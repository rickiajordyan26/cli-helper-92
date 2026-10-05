import logging
import os
from logging.handlers import RotatingFileHandler

class CreativeLogger:
    def __init__(self, name='cli-helper-92', path='logs/app.log'):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s'
        )

        rotator = RotatingFileHandler(
            path, maxBytes=1024 * 1024 * 5, backupCount=3
        )
        rotator.setFormatter(formatter)
        self.logger.addHandler(rotator)

    def get_logger(self):
        return self.logger

def setup_logging():
    return CreativeLogger().get_logger()

if __name__ == '__main__':
    log = setup_logging()
    log.info('System initialized with rotating log strategy')