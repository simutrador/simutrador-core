"""
Logging utilities for SimuTrador components.

This module provides standardized logging configuration that can be used
across all SimuTrador components for consistent logging behavior.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str,
    log_level: int = logging.INFO,
    log_dir: Optional[Path] = None,
    console_level: int = logging.INFO,
    file_level: int = logging.ERROR,
    max_bytes: int = 5 * 1024 * 1024,  # 5MB
    backup_count: int = 3,
) -> logging.Logger:
    """
    Set up a standardized logger for SimuTrador components.

    Args:
        name: Logger name (typically __name__ or component name)
        log_level: Overall logger level
        log_dir: Directory for log files (defaults to ./logs relative to caller)
        console_level: Console handler log level
        file_level: File handler log level
        max_bytes: Maximum size of log file before rotation
        backup_count: Number of backup files to keep

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Avoid adding duplicate handlers
    if logger.hasHandlers():
        return logger

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler (if log_dir is specified)
    if log_dir is not None:
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_dir / f"{name.replace('.', '_')}.log",
            maxBytes=max_bytes,
            backupCount=backup_count,
        )
        file_handler.setLevel(file_level)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


def get_default_logger(component_name: str) -> logging.Logger:
    """
    Get a default logger for a SimuTrador component.

    This creates a logger with standard settings:
    - INFO level console logging
    - ERROR level file logging to ./logs directory
    - Rotating file handler with 5MB max size

    Args:
        component_name: Name of the component (e.g., 'data_manager', 'simulator')

    Returns:
        Configured logger instance
    """
    log_dir = Path.cwd() / "logs"
    return setup_logger(
        name=component_name,
        log_level=logging.INFO,
        log_dir=log_dir,
        console_level=logging.INFO,
        file_level=logging.ERROR,
    )


def configure_third_party_loggers(level: int = logging.WARNING) -> None:
    """
    Configure third-party library loggers to reduce noise.

    Args:
        level: Log level to set for third-party loggers
    """
    # Common noisy loggers
    noisy_loggers = [
        "uvicorn.access",
        "httpx",
        "urllib3",
        "requests",
        "asyncio",
        "websockets",
    ]

    for logger_name in noisy_loggers:
        logging.getLogger(logger_name).setLevel(level)
