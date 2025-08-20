"""
Logging utilities for MKV Video Compressor.
"""

import logging
import logging.handlers
import os
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


def setup_logger(
    name: str = 'mkv_compressor',
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    console_output: bool = True,
    max_log_files: int = 10,
    max_file_size: int = 10 * 1024 * 1024  # 10MB
) -> logging.Logger:
    """
    Setup and configure logging for the application.
    
    Args:
        name: Logger name
        level: Logging level
        log_file: Path to log file. If None, uses default location.
        console_output: Whether to output to console
        max_log_files: Maximum number of log files to keep
        max_file_size: Maximum size of each log file in bytes
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Set logger level
    logger.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if log_file is None:
        # Use default log file location
        log_dir = get_log_directory()
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"{name}.log"
    
    try:
        # Use rotating file handler
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=max_log_files,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)  # File gets all levels
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    except Exception as e:
        # If file logging fails, at least log to console
        if console_output:
            logger.warning(f"Failed to setup file logging: {e}")
    
    # Log startup message
    logger.info(f"Logger initialized - Level: {logging.getLevelName(level)}")
    
    return logger


def get_log_directory() -> Path:
    """Get the application log directory."""
    if os.name == 'nt':  # Windows
        log_dir = Path.home() / "AppData" / "Local" / "MKV Compressor" / "logs"
    else:  # Unix/Linux/macOS
        log_dir = Path.home() / ".local" / "share" / "mkv-compressor" / "logs"
    
    return log_dir


def cleanup_old_logs(max_age_days: int = 30):
    """
    Clean up old log files.
    
    Args:
        max_age_days: Maximum age of log files to keep in days
    """
    try:
        log_dir = get_log_directory()
        if not log_dir.exists():
            return
        
        cutoff_time = datetime.now().timestamp() - (max_age_days * 24 * 60 * 60)
        
        for log_file in log_dir.glob("*.log*"):
            if log_file.stat().st_mtime < cutoff_time:
                log_file.unlink()
                
    except Exception as e:
        logging.warning(f"Failed to cleanup old logs: {e}")


class ProgressLogger:
    """Logger specifically for tracking progress of operations."""
    
    def __init__(self, logger: logging.Logger, operation_name: str):
        self.logger = logger
        self.operation_name = operation_name
        self.start_time = datetime.now()
        
    def log_start(self, message: str = ""):
        """Log operation start."""
        msg = f"Started {self.operation_name}"
        if message:
            msg += f": {message}"
        self.logger.info(msg)
    
    def log_progress(self, percentage: float, message: str = ""):
        """Log progress update."""
        msg = f"{self.operation_name} progress: {percentage:.1f}%"
        if message:
            msg += f" - {message}"
        self.logger.debug(msg)
    
    def log_complete(self, success: bool = True, message: str = ""):
        """Log operation completion."""
        elapsed = datetime.now() - self.start_time
        status = "completed" if success else "failed"
        
        msg = f"{self.operation_name} {status} in {elapsed.total_seconds():.1f}s"
        if message:
            msg += f": {message}"
        
        if success:
            self.logger.info(msg)
        else:
            self.logger.error(msg)


class FileOperationLogger:
    """Logger for file operations with automatic path sanitization."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def _sanitize_path(self, path: str) -> str:
        """Sanitize file path for logging (remove sensitive info)."""
        # Replace home directory with ~
        path_obj = Path(path)
        try:
            relative_to_home = path_obj.relative_to(Path.home())
            return f"~/{relative_to_home}"
        except ValueError:
            # Path is not relative to home, just return filename if it's very long
            if len(str(path_obj)) > 100:
                return f".../{path_obj.name}"
            return str(path_obj)
    
    def log_file_operation(self, operation: str, input_path: str, output_path: str = None):
        """Log a file operation."""
        input_sanitized = self._sanitize_path(input_path)
        
        if output_path:
            output_sanitized = self._sanitize_path(output_path)
            self.logger.info(f"{operation}: {input_sanitized} -> {output_sanitized}")
        else:
            self.logger.info(f"{operation}: {input_sanitized}")
    
    def log_file_error(self, operation: str, path: str, error: str):
        """Log a file operation error."""
        path_sanitized = self._sanitize_path(path)
        self.logger.error(f"{operation} failed for {path_sanitized}: {error}")


def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance with the default configuration.
    
    Args:
        name: Logger name. If None, uses the module name.
        
    Returns:
        Logger instance
    """
    if name is None:
        import inspect
        frame = inspect.currentframe().f_back
        name = frame.f_globals.get('__name__', 'mkv_compressor')
    
    return logging.getLogger(name)