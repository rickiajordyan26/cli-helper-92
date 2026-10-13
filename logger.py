import logging
from logging.handlers import RotatingFileHandler
import sys

def get_logger(name='cli-helper-92', log_file='app.log'):
    """Factory for a logger that plays musical chairs with log files."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # formatter for that 'professional' look
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s : %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # rotate logs: max 2MB, keep 5 history files
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=2*1024*1024, 
        backupCount=5
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # also shout to stdout because silence is boring
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # prevents duplicate logs from propagation mishaps
    logger.propagate = False
    
    return logger