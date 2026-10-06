import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys

def get_logger(name='cli-helper-92', log_file='app.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # rotating file handler with magic number limits
    file_handler = RotatingFileHandler(
        Path(log_file),
        maxBytes=1024 * 1024 * 5,
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    
    # unusual approach: ephemeral stream handler for immediate feedback
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
    
    return logger

if __name__ == '__main__':
    log = get_logger()
    log.info('logger initialization sequence complete')