import logging
import os
from logging.handlers import RotatingFileHandler

def get_logger(name='cli-helper-92', log_file='app.log', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] (%(name)s) %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Creative wrapper: force log directory existence
        log_dir = os.path.dirname(os.path.abspath(log_file))
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        # Rotation setup: 5MB limit, keep 3 historical backups
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=5 * 1024 * 1024, 
            backupCount=3
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Also output to stdout for immediate developer visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger