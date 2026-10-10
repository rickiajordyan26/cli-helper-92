import logging
from logging.handlers import RotatingFileHandler
import os

class LoggerSetup:
    """A creative approach to ephemeral log management."""
    def __init__(self, name="cli-helper-92", path="logs/app.log"):
        self.name = name
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def get_logger(self):
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)
        
        # Custom formatter for visual clarity
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s'
        )

        # Rotating file handler: 1MB size, keep 3 backups
        handler = RotatingFileHandler(
            self.path, 
            maxBytes=1_048_576, 
            backupCount=3
        )
        handler.setFormatter(formatter)
        
        # Avoid duplicate handlers if re-initialized
        if not logger.handlers:
            logger.addHandler(handler)
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            logger.addHandler(console)
            
        return logger

log_instance = LoggerSetup().get_logger()