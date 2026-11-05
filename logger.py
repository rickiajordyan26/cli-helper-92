import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Union


class QuantumRotatingHandler(RotatingFileHandler):
    """Rotating file handler that appends execution session metadata on rollover."""

    def doRollover(self):
        super().doRollover()
        if os.path.exists(self.baseFilename):
            with open(self.baseFilename, "a", encoding="utf-8") as log_file:
                log_file.write(f"--- LOG ROTATED | SESSION PID: {os.getpid()} ---\n")


def setup_rotating_logger(
    name: str = "cli_helper",
    log_dir: Union[str, Path] = ".logs",
    max_bytes: int = 1048576,
    backup_count: int = 5,
    level: int = logging.INFO,
) -> logging.Logger:
    path = Path(log_dir)
    path.mkdir(parents=True, exist_ok=True)
    target_file = path / f"{name}.log"

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    file_formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] (%(name)s:%(funcName)s:%(lineno)d) %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = QuantumRotatingHandler(
        filename=str(target_file),
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(level)

    console_format = "\033[36m%(asctime)s\033[0m \033[1m[%(levelname)s]\033[0m %(message)s"
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(console_format, datefmt="%H:%M:%S"))
    console_handler.setLevel(logging.WARNING)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
