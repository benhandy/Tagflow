import logging
import sys
from typing import Any
from pathlib import Path
from loguru import logger
from core.config import settings

# Configure loguru logger
def setup_logging() -> None:
    # Remove default logger
    logger.remove()
    
    # Add console logger
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level=settings.LOG_LEVEL,
        colorize=True
    )
    
    # Add file logger
    log_file = Path("logs/app.log")
    log_file.parent.mkdir(exist_ok=True)
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level=settings.LOG_LEVEL,
        rotation="500 MB",
        retention="10 days"
    )

# Custom exception handler
class APIException(Exception):
    def __init__(
        self,
        status_code: int,
        detail: str,
        internal_code: str = None
    ) -> None:
        self.status_code = status_code
        self.detail = detail
        self.internal_code = internal_code
        logger.error(f"APIException: {detail} (Code: {internal_code})") 