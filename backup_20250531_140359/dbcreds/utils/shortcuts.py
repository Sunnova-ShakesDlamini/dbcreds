# dbcreds/utils/shortcuts.py
"""
Convenience functions for common dbcreds operations.

This module provides simple shortcuts for the most common use cases,
making it easy to get started with dbcreds.
"""

from contextlib import contextmanager
from typing import Optional

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

