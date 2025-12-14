"""Logging Utilities"""
import logging
import sys
from typing import Optional

_loggers = {}

def setup_logger(name: str = "kuka_ml", level: int = logging.INFO,
                 log_file: Optional[str] = None) -> logging.Logger:
    """Set up logger with console and optional file output."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # File handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    _loggers[name] = logger
    return logger

def get_logger(name: str = "kuka_ml") -> logging.Logger:
    """Get existing logger or create new one."""
    if name not in _loggers:
        return setup_logger(name)
    return _loggers[name]
