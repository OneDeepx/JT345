"""
Logging Configuration
"""
from loguru import logger
from pathlib import Path
from config.settings import LOG_LEVEL, LOG_FORMAT, LOG_ROTATION


def setup_logger(name: str, log_file: Path = None):
    """
    Setup logger with file and console output
    
    Args:
        name: Logger name
        log_file: Path to log file
        
    Returns:
        Configured logger
    """
    # Remove default logger
    logger.remove()
    
    # Add console logger
    logger.add(
        sys.stderr,
        format=LOG_FORMAT,
        level=LOG_LEVEL,
        colorize=True
    )
    
    # Add file logger if specified
    if log_file:
        logger.add(
            log_file,
            format=LOG_FORMAT,
            level=LOG_LEVEL,
            rotation=LOG_ROTATION,
            compression="zip",
            retention="30 days"
        )
    
    return logger


import sys
