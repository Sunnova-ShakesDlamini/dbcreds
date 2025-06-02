# dbcreds/__init__.py
"""
dbcreds - Professional database credentials management.

This package provides secure credential storage and retrieval for database connections
with support for multiple environments and database types.
"""

import os
import sys

__version__ = "2.0.0"

# Check for fast mode
DBCREDS_FAST_MODE = os.environ.get('DBCREDS_FAST_MODE', '').lower() == 'true'
IS_MARIMO = any('marimo' in mod for mod in sys.modules)

# Use fast mode in marimo or when explicitly requested
USE_FAST_MODE = DBCREDS_FAST_MODE or IS_MARIMO

# Lazy loading state
_manager = None
_shortcuts_loaded = False
_logger_initialized = False


def _init_logger():
    """Initialize logger only when needed."""
    global _logger_initialized
    if _logger_initialized:
        return
    
    if not USE_FAST_MODE and os.getenv("DBCREDS_DEBUG"):
        from loguru import logger
        from rich.console import Console
        from rich.logging import RichHandler
        
        logger.remove()
        logger.add(
            RichHandler(console=Console(stderr=True), rich_tracebacks=True),
            format="{message}",
            level="DEBUG",
        )
    else:
        # Minimal logging in fast mode
        import sys
        from loguru import logger
        logger.remove()
        logger.add(sys.stderr, level="WARNING")
    
    _logger_initialized = True


def _ensure_shortcuts():
    """Lazy load shortcuts module."""
    global _shortcuts_loaded
    if not _shortcuts_loaded:
        # Import shortcuts functions into module namespace
        from dbcreds.utils.shortcuts import (
            get_async_engine as _get_async_engine,
            get_connection as _get_connection,
            get_connection_string as _get_connection_string,
            get_connection_string_fast as _get_connection_string_fast,
            get_credentials as _get_credentials,
            get_engine as _get_engine,
        )
        
        # Make them available at module level
        globals()['get_async_engine'] = _get_async_engine
        globals()['get_connection'] = _get_connection
        globals()['get_connection_string'] = _get_connection_string
        globals()['get_connection_string_fast'] = _get_connection_string_fast
        globals()['get_credentials'] = _get_credentials
        globals()['get_engine'] = _get_engine
        
        _shortcuts_loaded = True


def __getattr__(name):
    """Lazy load attributes on demand."""
    # Fast path for connection string in fast mode
    if USE_FAST_MODE and name == 'get_connection_string':
        from dbcreds.utils.shortcuts import get_connection_string_fast
        return get_connection_string_fast
    
    # Load shortcuts on first access
    if name in ['get_connection_string', 'get_credentials', 'get_engine', 
                'get_async_engine', 'get_connection', 'get_connection_string_fast']:
        _ensure_shortcuts()
        return globals()[name]
    
    # Load manager on demand
    if name == 'CredentialManager':
        if USE_FAST_MODE:
            # Return a lightweight error in fast mode
            raise ImportError(
                "CredentialManager not available in fast mode. "
                "Use get_connection_string() directly or set DBCREDS_FAST_MODE=false"
            )
        _init_logger()
        from dbcreds.core.manager import CredentialManager
        return CredentialManager
    
    # Load models on demand
    if name in ['DatabaseCredentials', 'DatabaseType', 'Environment']:
        from dbcreds.core import models
        return getattr(models, name)
    
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


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
