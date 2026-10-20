import logging
from logging.handlers import RotatingFileHandler
import sys
from pathlib import Path

class LoggerOrchestrator:
    def __init__(self, name: str = "cli-helper-92", log_file: str = "app.log"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        log_path = Path(log_file)
        log_path.touch(exist_ok=True)
        
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
        )

        file_handler = RotatingFileHandler(
            log_path, maxBytes=1_048_576, backupCount=3
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

setup = LoggerOrchestrator()
logger = setup.get_logger()