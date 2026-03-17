"""
Logging configuration for PDF crawler application.
Provides dual-level logging: DEBUG for all steps, ERROR for critical failures.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional


class CrawlerLogger:
    """Custom logger setup for the crawler application."""
    
    def __init__(self, name: str = 'pdf_crawler'):
        """Initialize logger.
        
        Args:
            name: Logger name
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self._configured = False
    
    def setup_logging(self, 
                     log_level: str = 'INFO',
                     log_file: Optional[str] = None,
                     console_output: bool = True) -> logging.Logger:
        """Configure logging with file and console handlers.
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional log file path
            console_output: Whether to output to console
            
        Returns:
            logging.Logger: Configured logger instance
        """
        if self._configured:
            return self.logger
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # Set logger level
        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError(f'Invalid log level: {log_level}')
        
        self.logger.setLevel(numeric_level)
        
        # Create formatter
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler for immediate feedback
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)  # Only INFO and above to console
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # File handler for detailed logging
        if log_file:
            self._setup_file_handler(log_file, formatter, numeric_level)
        
        self._configured = True
        return self.logger
    
    def _setup_file_handler(self, log_file: str, formatter: logging.Formatter, level: int):
        """Setup rotating file handler.
        
        Args:
            log_file: Log file path
            formatter: Log formatter
            level: Logging level
        """
        try:
            # Ensure log directory exists
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create rotating file handler (10MB max, 5 backups)
            file_handler = logging.handlers.RotatingFileHandler(
                filename=log_file,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            
            self.logger.debug(f"File logging initialized: {log_file}")
            
        except (OSError, PermissionError) as e:
            # If file logging fails, continue with console only
            self.logger.warning(f"Could not setup file logging {log_file}: {e}")
    
    def get_logger(self) -> logging.Logger:
        """Get the configured logger instance.
        
        Returns:
            logging.Logger: Logger instance
            
        Raises:
            RuntimeError: If logger hasn't been configured
        """
        if not self._configured:
            raise RuntimeError("Logger not configured. Call setup_logging() first.")
        return self.logger


def setup_application_logging(log_level: str = 'INFO', 
                            log_file: Optional[str] = None) -> logging.Logger:
    """Convenience function to setup application logging.
    
    Args:
        log_level: Logging level
        log_file: Optional log file path
        
    Returns:
        logging.Logger: Configured logger
    """
    logger_manager = CrawlerLogger('pdf_crawler')
    return logger_manager.setup_logging(log_level, log_file)


# Context manager for operation logging
class LoggedOperation:
    """Context manager for logging operation start/completion."""
    
    def __init__(self, logger: logging.Logger, operation: str):
        """Initialize logged operation.
        
        Args:
            logger: Logger instance
            operation: Operation description
        """
        self.logger = logger
        self.operation = operation
    
    def __enter__(self):
        """Log operation start."""
        self.logger.debug(f"Starting {self.operation}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Log operation completion or failure."""
        if exc_type is None:
            self.logger.debug(f"Completed {self.operation}")
        else:
            self.logger.error(f"Failed {self.operation}: {exc_val}")
        return False  # Don't suppress exceptions


# Utility functions for common logging patterns
def log_step(logger: logging.Logger, step: str, details: str = ""):
    """Log a processing step at DEBUG level.
    
    Args:
        logger: Logger instance
        step: Step description
        details: Optional additional details
    """
    message = f"STEP: {step}"
    if details:
        message += f" - {details}"
    logger.debug(message)


def log_progress(logger: logging.Logger, current: int, total: int, item: str = "items"):
    """Log progress information.
    
    Args:
        logger: Logger instance
        current: Current item number
        total: Total number of items
        item: Item type description
    """
    percentage = (current / total) * 100 if total > 0 else 0
    logger.debug(f"PROGRESS: {current}/{total} {item} ({percentage:.1f}%)")


def log_critical_error(logger: logging.Logger, operation: str, error: Exception):
    """Log a critical error that stops execution.
    
    Args:
        logger: Logger instance
        operation: Operation that failed
        error: Exception that occurred
    """
    logger.error(f"CRITICAL ERROR in {operation}: {type(error).__name__}: {error}")


def log_download_result(logger: logging.Logger, url: str, success: bool, 
                       filename: str = "", error_msg: str = ""):
    """Log download operation result.
    
    Args:
        logger: Logger instance
        url: URL that was downloaded
        success: Whether download succeeded
        filename: Downloaded filename (if successful)
        error_msg: Error message (if failed)
    """
    if success:
        logger.debug(f"DOWNLOAD SUCCESS: {url} -> {filename}")
    else:
        logger.error(f"DOWNLOAD FAILED: {url} - {error_msg}")
