#!/usr/bin/env python3
"""
Script to apply lazy loading changes to dbcreds for faster imports.
Run this in the root folder of the dbcreds project.
"""

import os
import shutil
from datetime import datetime
from pathlib import Path


def backup_file(filepath):
    """Create a backup of the file before modifying."""
    backup_path = f"{filepath}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(filepath, backup_path)
    print(f"✓ Backed up {filepath} to {backup_path}")
    return backup_path


def write_file(filepath, content):
    """Write content to file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Updated {filepath}")


# File contents for the updates
FILES_TO_UPDATE = {
    'dbcreds/__init__.py': '''# dbcreds/__init__.py
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
''',

    'dbcreds/core/manager.py': '''# dbcreds/core/manager.py
"""
Core credential manager implementation with lazy initialization.

This module provides the main CredentialManager class that orchestrates
credential storage and retrieval across different backends.
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Type

# Lazy imports to speed up module loading
_logger = None
_ValidationError = None
_models_loaded = False
_backends_loaded = False


def _get_logger():
    """Lazy load logger only when needed."""
    global _logger
    if _logger is None:
        from loguru import logger
        _logger = logger
    return _logger


def _load_models():
    """Lazy load models."""
    global _models_loaded, _ValidationError
    if not _models_loaded:
        from pydantic import ValidationError as _VE
        _ValidationError = _VE
        _models_loaded = True


class CredentialManager:
    """
    Main credential management class with lazy initialization.

    Orchestrates credential storage and retrieval across multiple backends,
    manages environments, and handles password expiration.

    Attributes:
        config_dir: Directory for configuration files
        backends: List of available credential backends
        environments: Dictionary of configured environments

    Examples:
        >>> manager = CredentialManager()
        >>> manager.add_environment("dev", DatabaseType.POSTGRESQL)
        >>> manager.set_credentials("dev", "localhost", 5432, "mydb", "user", "pass")
        >>> creds = manager.get_credentials("dev")
    """
    
    _instance = None
    _initialized = False

    def __new__(cls, config_dir: Optional[str] = None):
        """Singleton pattern with lazy initialization."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize the credential manager with lazy loading.

        Args:
            config_dir: Optional custom configuration directory. Defaults to ~/.dbcreds
        """
        # Only initialize once
        if self._initialized:
            return

        self.config_dir = config_dir or os.path.expanduser("~/.dbcreds")
        self.backends: List = []  # Avoid importing types
        self.environments: Dict[str, object] = {}  # Avoid importing Environment

        # Don't do anything heavy yet!
        self._initialized = True
        self._backends_initialized = False
        self._environments_loaded = False

    def _ensure_initialized(self):
        """Initialize backends and environments on first real use."""
        if not self._backends_initialized:
            os.makedirs(self.config_dir, exist_ok=True)
            self._initialize_backends()
            self._backends_initialized = True

        if not self._environments_loaded:
            self._load_environments()
            self._environments_loaded = True

    def _initialize_backends(self) -> None:
        """Initialize available credential backends in priority order."""
        # Import these only when actually initializing
        from dbcreds.backends.base import CredentialBackend
        
        backend_classes: List[Type[CredentialBackend]] = []

        # Platform-specific backends first
        if os.name == "nt":
            try:
                from dbcreds.backends.windows import WindowsCredentialBackend
                backend_classes.append(WindowsCredentialBackend)
            except ImportError:
                pass
            
            try:
                from dbcreds.backends.legacy_windows import LegacyWindowsBackend
                backend_classes.append(LegacyWindowsBackend)
            except ImportError:
                pass

        # Cross-platform backends
        try:
            from dbcreds.backends.keyring import KeyringBackend
            backend_classes.append(KeyringBackend)
        except ImportError:
            pass
            
        try:
            from dbcreds.backends.environment import EnvironmentBackend
            backend_classes.append(EnvironmentBackend)
        except ImportError:
            pass
            
        try:
            from dbcreds.backends.config import ConfigFileBackend
            backend_classes.append(ConfigFileBackend)
        except ImportError:
            pass

        for backend_class in backend_classes:
            try:
                backend = backend_class()
                if backend.is_available():
                    self.backends.append(backend)
                    _get_logger().debug(f"Initialized backend: {backend.__class__.__name__}")
            except Exception as e:
                _get_logger().debug(f"Failed to initialize {backend_class.__name__}: {e}")

        if not self.backends:
            _get_logger().warning(
                "No credential backends available, falling back to config file only"
            )
            from dbcreds.backends.config import ConfigFileBackend
            self.backends.append(ConfigFileBackend(self.config_dir))

    def _load_environments(self) -> None:
        """Load environment configurations from disk."""
        from dbcreds.backends.config import ConfigFileBackend
        from dbcreds.core.models import Environment
        
        _load_models()
        
        config_backend = ConfigFileBackend(self.config_dir)
        environments_data = config_backend.load_environments()

        for env_data in environments_data:
            try:
                env = Environment(**env_data)
                self.environments[env.name] = env
            except _ValidationError as e:
                _get_logger().error(f"Invalid environment data: {e}")

    def add_environment(
        self,
        name: str,
        database_type,  # Avoid importing DatabaseType
        description: Optional[str] = None,
        is_production: bool = False,
    ):
        """
        Add a new environment configuration.

        Args:
            name: Environment name (e.g., 'dev', 'prod')
            database_type: Type of database
            description: Optional description
            is_production: Whether this is a production environment

        Returns:
            Created Environment object

        Raises:
            CredentialError: If environment already exists

        Examples:
            >>> manager.add_environment("dev", DatabaseType.POSTGRESQL, "Development database")
        """
        self._ensure_initialized()
        
        from dbcreds.core.exceptions import CredentialError
        from dbcreds.core.models import Environment
        
        if name.lower() in self.environments:
            raise CredentialError(f"Environment '{name}' already exists")

        env = Environment(
            name=name.lower(),
            database_type=database_type,
            description=description,
            is_production=is_production,
        )

        self.environments[env.name] = env
        self._save_environments()

        _get_logger().info(f"Added environment: {env.name}")
        return env

    def remove_environment(self, name: str) -> None:
        """
        Remove an environment and its credentials.

        Args:
            name: Environment name to remove

        Raises:
            CredentialNotFoundError: If environment doesn't exist
        """
        self._ensure_initialized()
        
        from dbcreds.core.exceptions import CredentialNotFoundError
        
        env_name = name.lower()
        if env_name not in self.environments:
            raise CredentialNotFoundError(f"Environment '{name}' not found")

        # Remove credentials from all backends
        for backend in self.backends:
            try:
                backend.delete_credential(f"dbcreds:{env_name}")
            except Exception as e:
                _get_logger().debug(f"Failed to delete from {backend.__class__.__name__}: {e}")

        del self.environments[env_name]
        self._save_environments()

        _get_logger().info(f"Removed environment: {env_name}")

    def set_credentials(
        self,
        environment: str,
        host: str,
        port: int,
        database: str,
        username: str,
        password: str,
        password_expires_days: Optional[int] = 90,
        **options,
    ):
        """
        Store credentials for an environment.

        Args:
            environment: Environment name
            host: Database host
            port: Database port
            database: Database name
            username: Database username
            password: Database password
            password_expires_days: Days until password expires (None for no expiry)
            **options: Additional connection options

        Returns:
            Created DatabaseCredentials object

        Raises:
            CredentialNotFoundError: If environment doesn't exist

        Examples:
            >>> manager.set_credentials("dev", "localhost", 5432, "mydb", "user", "pass")
        """
        self._ensure_initialized()
        
        from dbcreds.core.exceptions import CredentialNotFoundError, CredentialError
        from dbcreds.core.models import DatabaseCredentials
        
        env_name = environment.lower()
        if env_name not in self.environments:
            raise CredentialNotFoundError(f"Environment '{environment}' not found")

        env = self.environments[env_name]

        # Calculate password expiration
        password_expires_at = None
        if password_expires_days:
            password_expires_at = datetime.now(timezone.utc) + timedelta(
                days=password_expires_days
            )

        # Create credentials object
        creds = DatabaseCredentials(
            environment=env_name,
            host=host,
            port=port,
            database=database,
            username=username,
            password=password,
            options=options,
            password_expires_at=password_expires_at,
        )

        # Store in backends
        stored = False
        for backend in self.backends:
            try:
                if backend.set_credential(
                    f"dbcreds:{env_name}", username, password, creds.model_dump()
                ):
                    stored = True
                    _get_logger().debug(f"Stored credentials in {backend.__class__.__name__}")
            except Exception as e:
                _get_logger().debug(f"Failed to store in {backend.__class__.__name__}: {e}")

        if not stored:
            raise CredentialError("Failed to store credentials in any backend")

        _get_logger().info(f"Stored credentials for environment: {env_name}")
        return creds

    def get_credentials(
        self, environment: str, check_expiry: bool = True
    ):
        """
        Retrieve credentials for an environment.

        Args:
            environment: Environment name
            check_expiry: Whether to check for password expiration

        Returns:
            DatabaseCredentials object

        Raises:
            CredentialNotFoundError: If credentials not found
            PasswordExpiredError: If password has expired

        Examples:
            >>> creds = manager.get_credentials("dev")
            >>> print(creds.host, creds.port)
        """
        self._ensure_initialized()
        
        from dbcreds.core.exceptions import CredentialNotFoundError, PasswordExpiredError
        from dbcreds.core.models import DatabaseCredentials
        
        env_name = environment.lower()
        if env_name not in self.environments:
            raise CredentialNotFoundError(f"Environment '{environment}' not found")

        # Try each backend
        for backend in self.backends:
            try:
                result = backend.get_credential(f"dbcreds:{env_name}")
                if result:
                    username, password, metadata = result
                    creds = DatabaseCredentials(
                        environment=env_name,
                        username=username,
                        password=password,
                        **metadata,
                    )

                    if check_expiry and creds.is_password_expired():
                        raise PasswordExpiredError(
                            f"Password for environment '{environment}' has expired"
                        )

                    _get_logger().debug(
                        f"Retrieved credentials from {backend.__class__.__name__}"
                    )
                    return creds
            except Exception as e:
                _get_logger().debug(f"Failed to get from {backend.__class__.__name__}: {e}")

        raise CredentialNotFoundError(
            f"No credentials found for environment '{environment}'"
        )

    def list_environments(self):
        """
        List all configured environments.

        Returns:
            List of Environment objects

        Examples:
            >>> envs = manager.list_environments()
            >>> for env in envs:
            ...     print(env.name, env.database_type)
        """
        self._ensure_initialized()
        return list(self.environments.values())

    def test_connection(self, environment: str) -> bool:
        """
        Test database connection for an environment.

        Args:
            environment: Environment name

        Returns:
            True if connection successful, False otherwise

        Examples:
            >>> if manager.test_connection("dev"):
            ...     print("Connection successful!")
        """
        self._ensure_initialized()
        
        from dbcreds.core.models import DatabaseType
        
        try:
            creds = self.get_credentials(environment)
            env = self.environments[environment.lower()]

            # Import appropriate database driver
            if env.database_type == DatabaseType.POSTGRESQL:
                import psycopg2

                conn = psycopg2.connect(
                    host=creds.host,
                    port=creds.port,
                    database=creds.database,
                    user=creds.username,
                    password=creds.password.get_secret_value(),
                )
                conn.close()
                return True
            # Add other database types as needed

        except Exception as e:
            _get_logger().error(f"Connection test failed for '{environment}': {e}")
            return False

    def _save_environments(self) -> None:
        """Save environment configurations to disk."""
        from dbcreds.backends.config import ConfigFileBackend
        
        config_backend = ConfigFileBackend(self.config_dir)
        config_backend.save_environments(
            [env.model_dump() for env in self.environments.values()]
        )
''',

    'dbcreds/utils/shortcuts.py': '''# dbcreds/utils/shortcuts.py
"""
Convenience functions for common dbcreds operations.

This module provides simple shortcuts for the most common use cases,
making it easy to get started with dbcreds.
"""

from contextlib import contextmanager
from typing import Any, Dict, Optional
import os
import ctypes
import ctypes.wintypes
import json
from functools import lru_cache

# Lazy imports
_sqlalchemy = None
_manager = None
_CredentialError = None


def _get_credential_error():
    """Lazy load CredentialError."""
    global _CredentialError
    if _CredentialError is None:
        from dbcreds.core.exceptions import CredentialError
        _CredentialError = CredentialError
    return _CredentialError


def _get_manager():
    """Get or create the global credential manager."""
    global _manager
    if _manager is None:
        from dbcreds.core.manager import CredentialManager
        _manager = CredentialManager()
    return _manager


@lru_cache(maxsize=10)
def get_connection_string_fast(environment: str = "default") -> str:
    """
    Get database connection string using fast, marimo-friendly method.
    
    This function bypasses the normal credential manager initialization
    and directly reads from environment variables or Windows Credential Manager.
    This is optimized for use in marimo notebooks where the standard import
    can cause hanging issues.
    
    Args:
        environment: Environment name (default: "default")
        
    Returns:
        Database connection URI
        
    Raises:
        ValueError: If credentials not found
        
    Examples:
        >>> # In a marimo notebook
        >>> from dbcreds import get_connection_string_fast
        >>> conn_string = get_connection_string_fast("fusionods")
    """
    # Check environment variables first
    conn_string = _get_from_environment(environment)
    if conn_string:
        return conn_string
    
    # Fall back to Windows Credential Manager
    if os.name == 'nt':
        conn_string = _get_from_windows_credential_manager(environment)
        if conn_string:
            return conn_string
    
    raise ValueError(
        f"No credentials found for environment '{environment}'. "
        "Please ensure credentials are set in environment variables or Windows Credential Manager."
    )


def _get_from_environment(env_name: str) -> Optional[str]:
    """Try to get connection from environment variables."""
    # Check if dbcreds has set environment variables
    prefix = f"DBCREDS_{env_name.upper()}_"
    
    # Also check legacy format (for PowerShell compatibility)
    legacy_vars = {
        'host': os.environ.get('DB_SERVER'),
        'port': os.environ.get('DB_PORT', '5432'),
        'database': os.environ.get('DB_NAME'),
        'username': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PWD'),
    }
    
    # Check new format
    new_vars = {
        'host': os.environ.get(f'{prefix}HOST'),
        'port': os.environ.get(f'{prefix}PORT', '5432'),
        'database': os.environ.get(f'{prefix}DATABASE'),
        'username': os.environ.get(f'{prefix}USERNAME'),
        'password': os.environ.get(f'{prefix}PASSWORD'),
    }
    
    # Use whichever has data
    vars_to_use = new_vars if new_vars['host'] else legacy_vars
    
    if all(vars_to_use.get(k) for k in ['host', 'database', 'username']):
        # Password might be in credential manager, but try env first
        if not vars_to_use.get('password') and os.name == 'nt':
            # Try to get from Windows Credential Manager
            cred_data = _read_windows_credential(f"dbcreds:{env_name}")
            if cred_data and cred_data.get('password'):
                vars_to_use['password'] = cred_data['password']
        
        if vars_to_use.get('password'):
            return (
                f"postgresql://{vars_to_use['username']}:{vars_to_use['password']}"
                f"@{vars_to_use['host']}:{vars_to_use['port']}/{vars_to_use['database']}"
            )
    
    return None


def _get_from_windows_credential_manager(env_name: str) -> Optional[str]:
    """Get connection string from Windows Credential Manager."""
    if os.name != 'nt':
        return None
    
    cred_data = _read_windows_credential(f"dbcreds:{env_name}")
    if cred_data and all(k in cred_data for k in ['username', 'password', 'host', 'database']):
        return (
            f"postgresql://{cred_data['username']}:{cred_data['password']}"
            f"@{cred_data['host']}:{cred_data.get('port', 5432)}/{cred_data['database']}"
        )
    
    return None


def _read_windows_credential(target: str) -> Dict[str, Any]:
    """Read credential from Windows Credential Manager using ctypes."""
    if os.name != 'nt':
        return {}
    
    class CREDENTIAL(ctypes.Structure):
        _fields_ = [
            ("Flags", ctypes.wintypes.DWORD),
            ("Type", ctypes.wintypes.DWORD),
            ("TargetName", ctypes.wintypes.LPWSTR),
            ("Comment", ctypes.wintypes.LPWSTR),
            ("LastWritten", ctypes.wintypes.FILETIME),
            ("CredentialBlobSize", ctypes.wintypes.DWORD),
            ("CredentialBlob", ctypes.POINTER(ctypes.c_char)),
            ("Persist", ctypes.wintypes.DWORD),
            ("AttributeCount", ctypes.wintypes.DWORD),
            ("Attributes", ctypes.c_void_p),
            ("TargetAlias", ctypes.wintypes.LPWSTR),
            ("UserName", ctypes.wintypes.LPWSTR),
        ]
    
    advapi32 = ctypes.windll.advapi32
    cred_ptr = ctypes.POINTER(CREDENTIAL)()
    
    CRED_TYPE_GENERIC = 1
    
    # Try to read the credential
    if advapi32.CredReadW(target, CRED_TYPE_GENERIC, 0, ctypes.byref(cred_ptr)):
        try:
            cred = cred_ptr.contents
            username = cred.UserName if cred.UserName else ""
            
            # Extract password from blob
            blob_size = cred.CredentialBlobSize
            if blob_size > 0:
                # Read the blob data
                blob_data = ctypes.string_at(cred.CredentialBlob, blob_size)
                
                # Try to decode as JSON first (dbcreds format)
                try:
                    blob_str = blob_data.decode('utf-16le', errors='ignore').rstrip('\\x00')
                    data = json.loads(blob_str)
                    password = data.get('password', '')
                    
                    # Get other metadata
                    return {
                        'username': username,
                        'password': password,
                        'host': data.get('host', ''),
                        'port': data.get('port', 5432),
                        'database': data.get('database', ''),
                    }
                except (json.JSONDecodeError, UnicodeDecodeError):
                    # Fallback: treat entire blob as password
                    password = blob_data.decode('utf-16le', errors='ignore').rstrip('\\x00')
                    return {
                        'username': username,
                        'password': password
                    }
            
            return {'username': username, 'password': ''}
            
        finally:
            advapi32.CredFree(cred_ptr)
    
    return {}


def get_credentials(environment: str = "default"):
    """
    Get database credentials for an environment.

    Args:
        environment: Environment name (default: "default")

    Returns:
        DatabaseCredentials object

    Examples:
        >>> creds = get_credentials("dev")
        >>> print(f"Connecting to {creds.host}:{creds.port}")
    """
    manager = _get_manager()
    return manager.get_credentials(environment)


def get_connection_string(environment: str = "default", include_password: bool = True) -> str:
    """
    Get a database connection string for an environment.

    Args:
        environment: Environment name (default: "default")
        include_password: Whether to include password in the string

    Returns:
        Database connection URI

    Examples:
        >>> uri = get_connection_string("dev")
        >>> print(uri)
        'postgresql://user:pass@localhost:5432/mydb'
    """
    # Try fast method first if we're in fast mode
    if os.environ.get('DBCREDS_FAST_MODE', '').lower() == 'true':
        return get_connection_string_fast(environment)
    
    creds = get_credentials(environment)
    return creds.get_connection_string(include_password=include_password)


@contextmanager
def get_connection(environment: str = "default", **kwargs):
    """
    Get a database connection for an environment.

    Args:
        environment: Environment name (default: "default")
        **kwargs: Additional connection parameters

    Yields:
        Database connection object

    Examples:
        >>> with get_connection("dev") as conn:
        ...     cursor = conn.cursor()
        ...     cursor.execute("SELECT 1")
    """
    manager = _get_manager()
    creds = manager.get_credentials(environment)
    env = manager.environments.get(environment.lower())

    if not env:
        raise _get_credential_error()(f"Environment '{environment}' not found")

    # Import DatabaseType only when needed
    from dbcreds.core.models import DatabaseType
    
    # Get appropriate connection based on database type
    if env.database_type == DatabaseType.POSTGRESQL:
        import psycopg2

        conn_params = {
            "host": creds.host,
            "port": creds.port,
            "database": creds.database,
            "user": creds.username,
            "password": creds.password.get_secret_value(),
            **kwargs,
        }
        conn = psycopg2.connect(**conn_params)
        try:
            yield conn
        finally:
            conn.close()

    elif env.database_type == DatabaseType.MYSQL:
        import MySQLdb

        conn_params = {
            "host": creds.host,
            "port": creds.port,
            "db": creds.database,
            "user": creds.username,
            "passwd": creds.password.get_secret_value(),
            **kwargs,
        }
        conn = MySQLdb.connect(**conn_params)
        try:
            yield conn
        finally:
            conn.close()

    else:
        raise NotImplementedError(f"Database type {env.database_type} not yet implemented")


def get_engine(environment: str = "default", **kwargs):
    """
    Get a SQLAlchemy engine for an environment.

    Args:
        environment: Environment name (default: "default")
        **kwargs: Additional engine parameters

    Returns:
        SQLAlchemy Engine object

    Examples:
        >>> engine = get_engine("dev")
        >>> with engine.connect() as conn:
        ...     result = conn.execute("SELECT 1")
    """
    global _sqlalchemy
    if _sqlalchemy is None:
        from sqlalchemy import create_engine
        _sqlalchemy = create_engine
    
    conn_string = get_connection_string(environment)
    return _sqlalchemy(conn_string, **kwargs)


async def get_async_engine(environment: str = "default", **kwargs):
    """
    Get an async SQLAlchemy engine for an environment.

    Args:
        environment: Environment name (default: "default")
        **kwargs: Additional engine parameters

    Returns:
        SQLAlchemy AsyncEngine object

    Examples:
        >>> engine = await get_async_engine("dev")
        >>> async with engine.connect() as conn:
        ...     result = await conn.execute("SELECT 1")
    """
    from sqlalchemy.ext.asyncio import create_async_engine
    
    manager = _get_manager()
    creds = manager.get_credentials(environment)
    env = manager.environments.get(environment.lower())

    if not env:
        raise _get_credential_error()(f"Environment '{environment}' not found")

    # Import DatabaseType only when needed
    from dbcreds.core.models import DatabaseType
    
    # Build async connection string
    if env.database_type == DatabaseType.POSTGRESQL:
        driver = "postgresql+asyncpg"
    elif env.database_type == DatabaseType.MYSQL:
        driver = "mysql+aiomysql"
    else:
        raise NotImplementedError(f"Async support for {env.database_type} not yet implemented")

    conn_string = f"{driver}://{creds.username}:{creds.password.get_secret_value()}@{creds.host}:{creds.port}/{creds.database}"
    return create_async_engine(conn_string, **kwargs)
''',
}


def main():
    """Apply lazy loading changes to dbcreds."""
    print("🚀 Applying lazy loading optimizations to dbcreds...")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists('pyproject.toml'):
        print("❌ Error: pyproject.toml not found. Are you in the dbcreds root directory?")
        return 1
    
    # Check if dbcreds package exists
    if not os.path.exists('dbcreds'):
        print("❌ Error: dbcreds package directory not found.")
        return 1
    
    # Process each file
    for filepath, content in FILES_TO_UPDATE.items():
        full_path = Path(filepath)
        
        # Create directories if they don't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Backup existing file if it exists
        if full_path.exists():
            backup_file(full_path)
        
        # Write new content
        write_file(full_path, content)
    
    print()
    print("✨ Lazy loading optimizations applied successfully!")
    print()
    print("📝 Usage notes:")
    print("   - Normal usage: from dbcreds import get_connection_string")
    print("   - Fast mode: export DBCREDS_FAST_MODE=true")
    print("   - Marimo: Automatically uses fast mode")
    print("   - Direct fast: from dbcreds import get_connection_string_fast")
    print()
    print("🔧 Test with:")
    print("   python -c \"import time; start=time.time(); from dbcreds import get_connection_string; print(f'Import took {time.time()-start:.3f}s')\"")
    
    return 0


if __name__ == "__main__":
    exit(main())