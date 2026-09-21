import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name: str, log_file: str = 'app.log') -> logging.Logger:
    """
    A moody logger that enjoys rotating its own history.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
        )

        # Rotate every 1MB, keeping 3 backups
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=1024*1024, 
            backupCount=3
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Also stream to console for immediate satisfaction
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

# Quick invocation example for internal testing
if __name__ == '__main__':
    log = get_logger('cli-helper-92')
    log.info('System initialization complete')