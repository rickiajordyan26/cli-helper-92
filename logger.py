import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

class EmojiRotatorFormatter(logging.Formatter):
    EMOJI_MAP = {
        logging.DEBUG: "🔍",
        logging.INFO: "💡",
        logging.WARNING: "⚠️",
        logging.ERROR: "🚨",
        logging.CRITICAL: "💥",
    }

    def format(self, record: logging.LogRecord) -> str:
        icon = self.EMOJI_MAP.get(record.levelno, "📌")
        record.msg = f"{icon} [{record.levelname}] {record.msg}"
        return super().format(record)

def setup_cli_logger(
    app_name: str = "cli-helper-92",
    log_dir: str = ".logs",
    max_bytes: int = 5120,
    backup_count: int = 3
) -> logging.Logger:
    path = Path(log_dir)
    path.mkdir(parents=True, exist_ok=True)
    log_file = path / f"{app_name}.log"

    logger = logging.getLogger(app_name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(EmojiRotatorFormatter("%(message)s"))
    console_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

main_logger = setup_cli_logger()