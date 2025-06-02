# dbcreds/__init__.py
"""
dbcreds - Professional database credentials management.

This package provides secure credential storage and retrieval for database connections
with support for multiple environments and database types.
"""

import os
import sys

from loguru import logger
from rich.console import Console
from rich.logging import RichHandler

from dbcreds.core.manager import CredentialManager
from dbcreds.core.models import DatabaseCredentials, DatabaseType, Environment
from dbcreds.utils.shortcuts import (
    get_async_engine,
    get_connection,
    get_connection_string,
    get_connection_string_fast,  
    get_credentials,
    get_engine,
)

__version__ = "2.0.0"
__all__ = [
    "CredentialManager",
    "DatabaseCredentials",
    "DatabaseType",
    "Environment",
    "get_connection",
    "get_engine",
    "get_async_engine",
    "get_credentials",
    "get_connection_string",
     "get_connection_string_fast",
]

# Configure logger with rich handler
logger.remove()  # Remove default handler

if os.getenv("DBCREDS_DEBUG"):
    # Debug mode with rich formatting
    logger.add(
        RichHandler(console=Console(stderr=True), rich_tracebacks=True),
        format="{message}",
        level="DEBUG",
    )
else:
    # Production mode - minimal logging
    logger.add(sys.stderr, level="WARNING")