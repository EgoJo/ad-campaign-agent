"""
File logging configuration for logs service.

Configures JSON-structured rotating file logs.
"""

import logging
import logging.handlers
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON line."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "service": getattr(record, "service", "logs_service"),
            "stage": getattr(record, "stage", "orchestrator"),
            "message": record.getMessage(),
            "correlation_id": getattr(record, "correlation_id", None),
            "context": getattr(record, "context", {})
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)


def setup_file_logging(log_file_path: str = "logs/logs_service.log") -> logging.Logger:
    """
    Set up rotating file logging with JSON format.
    
    Args:
        log_file_path: Path to log file
        
    Returns:
        Configured logger instance
    """
    # Ensure logs directory exists
    log_dir = Path(log_file_path).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("logs_service_file")
    logger.setLevel(logging.INFO)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Create rotating file handler
    handler = logging.handlers.RotatingFileHandler(
        filename=log_file_path,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    
    # Set JSON formatter
    handler.setFormatter(JSONFormatter())
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger


def log_event_to_file(
    logger: logging.Logger,
    timestamp: str,
    stage: str,
    service: str,
    level: str,
    message: str,
    context: Dict[str, Any],
    correlation_id: str = None
):
    """
    Write a log event to file using the configured logger.
    
    Args:
        logger: Configured logger instance
        timestamp: Event timestamp
        stage: Workflow stage
        service: Service name
        level: Log level
        message: Event message
        context: Event context (request/response/metadata)
        correlation_id: Optional correlation ID
    """
    extra = {
        "service": service,
        "stage": stage,
        "correlation_id": correlation_id,
        "context": context
    }
    
    log_method = getattr(logger, level.lower(), logger.info)
    log_method(message, extra=extra)

