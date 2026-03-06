"""
Logging Configuration and Management

This module provides centralised logging configuration and management for the application.
Configures logging formats, handlers, and log file management to ensure consistent
logging across all application components.

Features:
    - Standardised log formatting
    - File-based logging with rotation
    - Log level management
    - Thread-safe logging operations

Exports:
    logger: Configured logger instance for use across the application

Usage:
    from logmanager import logger

    logger.info('Operation completed successfully')
    logger.warning('Resource threshold reached')
    logger.error('Failed to complete operation')

Log Format:
    Timestamps, log levels, and contextual information are automatically included
    in each log entry for effective debugging and monitoring.

Log Files:
    Logs are stored with automatic rotation to prevent excessive disk usage
    while maintaining historical records.
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from app_control import settings

# Ensure log directory exists
log_dir = os.path.dirname(settings['logfilepath'])
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger = logging.getLogger(settings['logappname'])
"""
Usage:\n
**logger.info('message')** for info messages\n
**logger.warning('message')** for warnings\n
**logger.error('message')** for errors
"""

if settings['loglevel'].upper() == 'DEBUG':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

LogFile = RotatingFileHandler(settings['logfilepath'], maxBytes=1048576, backupCount=10)
formatter = logging.Formatter('%(asctime)s, %(name)s, %(levelname)s : %(message)s')
LogFile.setFormatter(formatter)
logger.addHandler(LogFile)
logger.info('Runnng Python %s on %s', sys.version, sys.platform)
logger.info('Logging level set to: %s',settings['loglevel'].upper())
