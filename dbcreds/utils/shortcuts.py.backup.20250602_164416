# dbcreds/utils/shortcuts.py
# dbcreds/utils/shortcuts.py
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

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from dbcreds.core.exceptions import CredentialError
from dbcreds.core.manager import CredentialManager
from dbcreds.core.models import DatabaseCredentials, DatabaseType

# Global credential manager instance
_manager: Optional[CredentialManager] = None


def _get_manager() -> CredentialManager:
    """Get or create the global credential manager."""
    global _manager
    if _manager is None:
        _manager = CredentialManager()
    return _manager


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
        CredentialError: If credentials not found
        
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
    
    raise CredentialError(
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
                    blob_str = blob_data.decode('utf-16le', errors='ignore').rstrip('\x00')
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
                    password = blob_data.decode('utf-16le', errors='ignore').rstrip('\x00')
                    return {
                        'username': username,
                        'password': password
                    }
            
            return {'username': username, 'password': ''}
            
        finally:
            advapi32.CredFree(cred_ptr)
    
    return {}




def get_credentials(environment: str = "default") -> DatabaseCredentials:
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
        raise CredentialError(f"Environment '{environment}' not found")

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


def get_engine(environment: str = "default", **kwargs) -> Engine:
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
    conn_string = get_connection_string(environment)
    return create_engine(conn_string, **kwargs)


async def get_async_engine(environment: str = "default", **kwargs) -> AsyncEngine:
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
    manager = _get_manager()
    creds = manager.get_credentials(environment)
    env = manager.environments.get(environment.lower())

    if not env:
        raise CredentialError(f"Environment '{environment}' not found")

    # Build async connection string
    if env.database_type == DatabaseType.POSTGRESQL:
        driver = "postgresql+asyncpg"
    elif env.database_type == DatabaseType.MYSQL:
        driver = "mysql+aiomysql"
    else:
        raise NotImplementedError(f"Async support for {env.database_type} not yet implemented")

    conn_string = f"{driver}://{creds.username}:{creds.password.get_secret_value()}@{creds.host}:{creds.port}/{creds.database}"
    return create_async_engine(conn_string, **kwargs)

