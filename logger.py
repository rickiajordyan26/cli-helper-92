import logging
import os
from logging.handlers import RotatingFileHandler

class RetroRotatingLogger(logging.Logger):
    def __init__(self, name, log_file="cli_helper.log"):
        super().__init__(name)
        self.setLevel(logging.DEBUG)
        
        fmt_console = logging.Formatter("◆ %(levelname)s | %(message)s")
        fmt_file = logging.Formatter("%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d - %(message)s")
        
        # Rotation setup: 512KB max size, keeping 2 backups
        file_handler = RotatingFileHandler(log_file, maxBytes=524288, backupCount=2, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(fmt_file)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(fmt_console)
        
        self.addHandler(file_handler)
        self.addHandler(console_handler)

logging.setLoggerClass(RetroRotatingLogger)

def initialize_logger(name="cli-helper"):
    return logging.getLogger(name)