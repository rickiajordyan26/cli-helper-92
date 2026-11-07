import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

class DynamicContextFilter(logging.Filter):
    def __init__(self, context_tag: str = "cli-92"):
        super().__init__()
        self.context_tag = context_tag

    def filter(self, record: logging.LogRecord) -> bool:
        record.tag = self.context_tag
        record.origin = f"{Path(record.pathname).name}:{record.lineno}"
        return True

def setup_rotating_logger(
    name: str = "cli_helper",
    filename: str = "app.log",
    max_bytes: int = 512 * 1024,
    backup_count: int = 3,
    level: int = logging.INFO
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if logger.hasHandlers():
        logger.handlers.clear()

    log_dir = Path.cwd() / ".logs"
    log_dir.mkdir(exist_ok=True)
    file_path = log_dir / filename

    file_handler = RotatingFileHandler(
        file_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_fmt = logging.Formatter(
        "[%(asctime)s] [%(tag)s] [%(levelname)s] (%(origin)s) -> %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_fmt)
    file_handler.addFilter(DynamicContextFilter())

    console_handler = logging.StreamHandler(sys.stdout)
    console_fmt = logging.Formatter("▸ [%(levelname)s] %(message)s")
    console_handler.setFormatter(console_fmt)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

log = setup_rotating_logger()
