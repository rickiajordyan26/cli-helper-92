import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

class PaletteFormatter(logging.Formatter):
    """Custom formatter injecting ANSI log colors into terminal streams."""
    COLORS = {
        logging.DEBUG: "\033[36m",    # Cyan
        logging.INFO: "\033[32m",     # Green
        logging.WARNING: "\033[33m",  # Yellow
        logging.ERROR: "\033[31m",    # Red
        logging.CRITICAL: "\033[35m", # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, self.RESET)
        original_level = record.levelname
        record.levelname = f"{color}{record.levelname:<8}{self.RESET}"
        formatted = super().format(record)
        record.levelname = original_level
        return formatted

def setup_rotating_logger(
    app_name: str = "cli_helper",
    log_dir: str = ".logs",
    max_bytes: int = 512 * 1024,
    backup_count: int = 3
) -> logging.Logger:
    """Initializes dual console and size-rotated file loggers."""
    target_dir = Path(log_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    log_file = target_dir / f"{app_name}.log"

    logger = logging.getLogger(app_name)
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    log_format = "%(asctime)s | %(levelname)s | %(name)s :: %(message)s"
    file_formatter = logging.Formatter(log_format)
    
    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(PaletteFormatter(log_format))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

if __name__ == "__main__":
    log = setup_rotating_logger()
    log.info("rotating logger subsystem ready")
    log.warning("storage capacity approaching threshold")
