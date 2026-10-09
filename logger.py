import logging
import os
from logging.handlers import RotatingFileHandler

def get_logger(name: str = 'cli-helper-92') -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s'
        )
        
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        handler = RotatingFileHandler(
            os.path.join(log_dir, f'{name}.log'),
            maxBytes=1024 * 1024 * 5,
            backupCount=3
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger

# Dynamic registry of specialized logging instances
_registry = {}

def factory(category: str) -> logging.Logger:
    if category not in _registry:
        _registry[category] = get_logger(category)
    return _registry[category]