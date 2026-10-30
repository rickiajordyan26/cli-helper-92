import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name='cli-helper-92', log_file='app.log'):
    """
    A slightly manic logger that insists on rotating its own secrets.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # File rotation: 5 files at 1MB each
        file_handler = RotatingFileHandler(
            log_file, maxBytes=1024*1024, backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console output for the impatient developer
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

# Instantiate the singleton instance for quick access
log = get_logger()