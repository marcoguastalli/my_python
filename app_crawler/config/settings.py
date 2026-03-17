"""
Configuration management for PDF crawler application.
Handles .env file loading, validation, and provides type-safe configuration access.
"""

import os
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
import urllib.parse


@dataclass
class CrawlerConfig:
    """Configuration data class with validation."""
    
    # Crawler settings
    endpoint: str
    extension: str
    timeout_in_seconds: int
    
    # Downloader settings  
    target_folder: str
    fail_on_error: bool
    
    # Logging settings
    log_level: str
    log_file: str
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        self._validate_endpoint()
        self._validate_extension()
        self._validate_timeout()
        self._validate_target_folder()
        self._validate_log_level()
    
    def _validate_endpoint(self):
        """Validate endpoint URL."""
        if not self.endpoint:
            raise ValueError("ENDPOINT cannot be empty")
        
        parsed = urllib.parse.urlparse(self.endpoint)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid ENDPOINT URL format: {self.endpoint}")
        
        if parsed.scheme not in ['http', 'https']:
            raise ValueError(f"ENDPOINT must use HTTP or HTTPS protocol: {self.endpoint}")
    
    def _validate_extension(self):
        """Validate file extension."""
        if not self.extension:
            raise ValueError("EXTENSION cannot be empty")
        
        # Remove leading dot if present
        self.extension = self.extension.lstrip('.')
        
        if not self.extension.isalnum():
            raise ValueError(f"EXTENSION must be alphanumeric: {self.extension}")
    
    def _validate_timeout(self):
        """Validate timeout value."""
        if self.timeout_in_seconds <= 0:
            raise ValueError(f"TIMEOUT_IN_SECONDS must be positive: {self.timeout_in_seconds}")
        
        if self.timeout_in_seconds > 3600:  # 1 hour max
            raise ValueError(f"TIMEOUT_IN_SECONDS too large (max 3600): {self.timeout_in_seconds}")
    
    def _validate_target_folder(self):
        """Validate and expand target folder path."""
        if not self.target_folder:
            raise ValueError("TARGET_FOLDER cannot be empty")
        
        # Expand user home directory
        expanded_path = os.path.expanduser(self.target_folder)
        self.target_folder = os.path.abspath(expanded_path)
        
        # Create directory if it doesn't exist
        try:
            Path(self.target_folder).mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError) as e:
            raise ValueError(f"Cannot create TARGET_FOLDER {self.target_folder}: {e}")
    
    def _validate_log_level(self):
        """Validate log level."""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        self.log_level = self.log_level.upper()
        
        if self.log_level not in valid_levels:
            raise ValueError(f"LOG_LEVEL must be one of {valid_levels}: {self.log_level}")


class ConfigManager:
    """Manages application configuration loading and validation."""
    
    def __init__(self, env_file: str = '.env'):
        """Initialize configuration manager.
        
        Args:
            env_file: Path to environment file
        """
        self.env_file = env_file
        self._config: Optional[CrawlerConfig] = None
    
    def load_config(self) -> CrawlerConfig:
        """Load and validate configuration from .env file.
        
        Returns:
            CrawlerConfig: Validated configuration object
            
        Raises:
            FileNotFoundError: If .env file doesn't exist
            ValueError: If configuration is invalid
        """
        if not os.path.exists(self.env_file):
            raise FileNotFoundError(f"Environment file not found: {self.env_file}")
        
        # Load environment variables
        load_dotenv(self.env_file, override=True)
        
        try:
            self._config = CrawlerConfig(
                # Crawler settings
                endpoint=self._get_env_var('ENDPOINT'),
                extension=self._get_env_var('EXTENSION'),
                timeout_in_seconds=self._get_env_int('TIMEOUT_IN_SECONDS'),
                
                # Downloader settings
                target_folder=self._get_env_var('TARGET_FOLDER'),
                fail_on_error=self._get_env_bool('FAIL_ON_ERROR'),
                
                # Logging settings
                log_level=self._get_env_var('LOG_LEVEL', 'INFO'),
                log_file=self._get_env_var('LOG_FILE', 'app_crawler.log')
            )
            
            return self._config
            
        except ValueError as e:
            raise ValueError(f"Configuration validation failed: {e}")
    
    def _get_env_var(self, key: str, default: Optional[str] = None) -> str:
        """Get environment variable with optional default.
        
        Args:
            key: Environment variable key
            default: Default value if not found
            
        Returns:
            str: Environment variable value
            
        Raises:
            ValueError: If required variable is missing
        """
        value = os.getenv(key, default)
        if value is None:
            raise ValueError(f"Required environment variable missing: {key}")
        return value.strip()
    
    def _get_env_int(self, key: str, default: Optional[int] = None) -> int:
        """Get integer environment variable.
        
        Args:
            key: Environment variable key
            default: Default value if not found
            
        Returns:
            int: Environment variable value as integer
            
        Raises:
            ValueError: If variable is missing or not a valid integer
        """
        value = os.getenv(key)
        if value is None:
            if default is not None:
                return default
            raise ValueError(f"Required environment variable missing: {key}")
        
        try:
            return int(value.strip())
        except ValueError:
            raise ValueError(f"Environment variable {key} must be an integer: {value}")
    
    def _get_env_bool(self, key: str, default: bool = False) -> bool:
        """Get boolean environment variable.
        
        Args:
            key: Environment variable key
            default: Default value if not found
            
        Returns:
            bool: Environment variable value as boolean
        """
        value = os.getenv(key)
        if value is None:
            return default
        
        return value.strip().lower() in ('true', '1', 'yes', 'on')
    
    def get_config(self) -> CrawlerConfig:
        """Get current configuration.
        
        Returns:
            CrawlerConfig: Current configuration
            
        Raises:
            RuntimeError: If configuration hasn't been loaded
        """
        if self._config is None:
            raise RuntimeError("Configuration not loaded. Call load_config() first.")
        return self._config


# Example .env file content for reference
ENV_TEMPLATE = """
# Crawler Configuration
ENDPOINT=https://archive.org/details/kappa-magazine
EXTENSION=pdf
TIMEOUT_IN_SECONDS=300

# Downloader Configuration
TARGET_FOLDER=~/Downloads
FAIL_ON_ERROR=false

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=app_crawler.log
"""
