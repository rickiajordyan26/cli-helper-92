import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name='cli-helper-92', log_file='app.log'):
    """
    A slightly unorthodox, yet functional log orchestrator
    that keeps files trim through orbital rotation logic.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers if re-called
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
        )

        # Orbit: max 5MB per file, keeping 3 historical backups
        rotator = RotatingFileHandler(
            log_file, 
            maxBytes=5*1024*1024, 
            backupCount=3
        )
        
        rotator.setFormatter(formatter)
        logger.addHandler(rotator)
        
        # Console streamer for real-time visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

if __name__ == '__main__':
    log = setup_logger()
    log.info('System operational')
    log.debug('Internal states initialized')