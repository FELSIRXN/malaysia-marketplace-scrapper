"""
Professional logging utility for the multi-platform e-commerce scraper.
Provides clean, structured logging without emojis for production use.
"""

import logging
import logging.config
import os
from datetime import datetime
from typing import Optional
from config import LOGGING_CONFIG, OUTPUT_DIRS


class ScraperLogger:
    """Centralized logger for the scraper application."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ScraperLogger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.setup_logging()
            self._initialized = True
    
    def setup_logging(self):
        """Initialize logging configuration."""
        # Create logs directory if it doesn't exist
        logs_dir = OUTPUT_DIRS['logs']
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        # Configure logging
        logging.config.dictConfig(LOGGING_CONFIG)
        self.logger = logging.getLogger(__name__)
        
        # Log startup
        self.logger.info("Scraper logging system initialized")
    
    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """Get a logger instance for a specific module."""
        if name:
            return logging.getLogger(name)
        return self.logger
    
    def log_search_start(self, platform: str, keyword: str, limit: int):
        """Log the start of a search operation."""
        self.logger.info(f"Starting search on {platform} for '{keyword}' (limit: {limit})")
    
    def log_search_complete(self, platform: str, results_count: int, duration: float):
        """Log the completion of a search operation."""
        self.logger.info(f"Search completed on {platform}: {results_count} results in {duration:.2f}s")
    
    def log_search_error(self, platform: str, error: str):
        """Log a search error."""
        self.logger.error(f"Search failed on {platform}: {error}")
    
    def log_analysis_start(self, analysis_type: str, data_count: int):
        """Log the start of an analysis operation."""
        self.logger.info(f"Starting {analysis_type} analysis on {data_count} items")
    
    def log_analysis_complete(self, analysis_type: str, duration: float):
        """Log the completion of an analysis operation."""
        self.logger.info(f"{analysis_type} analysis completed in {duration:.2f}s")
    
    def log_export_start(self, format_type: str, filename: str):
        """Log the start of a data export."""
        self.logger.info(f"Starting export to {format_type} format: {filename}")
    
    def log_export_complete(self, filename: str, size: int):
        """Log the completion of a data export."""
        self.logger.info(f"Export completed: {filename} ({size} bytes)")
    
    def log_platform_error(self, platform: str, error_type: str, details: str):
        """Log platform-specific errors."""
        self.logger.error(f"Platform error [{platform}] {error_type}: {details}")
    
    def log_request_details(self, method: str, url: str, status_code: int, duration: float):
        """Log HTTP request details."""
        self.logger.debug(f"{method} {url} -> {status_code} ({duration:.2f}s)")
    
    def log_rate_limit(self, platform: str, delay: float):
        """Log rate limiting events."""
        self.logger.warning(f"Rate limited on {platform}, delaying {delay}s")
    
    def log_data_validation(self, validation_type: str, passed: bool, details: str = ""):
        """Log data validation results."""
        level = "info" if passed else "warning"
        status = "passed" if passed else "failed"
        message = f"Data validation {status}: {validation_type}"
        if details:
            message += f" - {details}"
        getattr(self.logger, level)(message)
    
    def log_configuration(self, config_dict: dict):
        """Log current configuration."""
        self.logger.info("Configuration loaded:")
        for key, value in config_dict.items():
            if 'password' not in key.lower() and 'key' not in key.lower():
                self.logger.info(f"  {key}: {value}")
    
    def log_performance_metric(self, metric_name: str, value: float, unit: str = ""):
        """Log performance metrics."""
        self.logger.info(f"Performance metric - {metric_name}: {value}{unit}")
    
    def log_cleanup_start(self, operation: str):
        """Log the start of cleanup operations."""
        self.logger.info(f"Starting cleanup: {operation}")
    
    def log_cleanup_complete(self, operation: str, items_cleaned: int):
        """Log the completion of cleanup operations."""
        self.logger.info(f"Cleanup completed: {operation} ({items_cleaned} items)")


# Global logger instance
scraper_logger = ScraperLogger()

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger instance."""
    return scraper_logger.get_logger(name)

def log_search_start(platform: str, keyword: str, limit: int):
    """Log search start."""
    scraper_logger.log_search_start(platform, keyword, limit)

def log_search_complete(platform: str, results_count: int, duration: float):
    """Log search completion."""
    scraper_logger.log_search_complete(platform, results_count, duration)

def log_search_error(platform: str, error: str):
    """Log search error."""
    scraper_logger.log_search_error(platform, error)

def log_analysis_start(analysis_type: str, data_count: int):
    """Log analysis start."""
    scraper_logger.log_analysis_start(analysis_type, data_count)

def log_analysis_complete(analysis_type: str, duration: float):
    """Log analysis completion."""
    scraper_logger.log_analysis_complete(analysis_type, duration)

def log_export_start(format_type: str, filename: str):
    """Log export start."""
    scraper_logger.log_export_start(format_type, filename)

def log_export_complete(filename: str, size: int):
    """Log export completion."""
    scraper_logger.log_export_complete(filename, size)

def log_platform_error(platform: str, error_type: str, details: str):
    """Log platform error."""
    scraper_logger.log_platform_error(platform, error_type, details)

def log_configuration(config_dict: dict):
    """Log configuration."""
    scraper_logger.log_configuration(config_dict)
