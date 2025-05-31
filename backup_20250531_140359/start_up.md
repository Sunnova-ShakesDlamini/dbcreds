# dbcreds Reference

Auto-generated on 2025-05-31 13:09:48

This file contains the latest source code for the dbcreds library.


## Directory Structure

Project organization showing the key files and their relationships:


```
dbcreds/
├── __init__.py
├── cli.py
├── migrate.py
├── backends/
│   ├── __init__.py
│   ├── base.py
│   ├── config.py
│   ├── environment.py
│   ├── keyring.py
│   ├── legacy_windows.py
│   └── windows.py
├── core/
│   ├── __init__.py
│   ├── exceptions.py
│   ├── manager.py
│   ├── models.py
│   └── security.py
├── utils/
│   ├── __init__.py
│   └── shortcuts.py
└── web/
    ├── __init__.py
    ├── __main__.py
    ├── auth.py
    ├── errors.py
    ├── main.py
    └── templates/
        ├── base.html
        ├── index.html
        ├── settings.html
        └── partials/
            └── environment_list.html
```

```toml # pyproject.toml
# pyproject.toml
[project]
name = "dbcreds"
version = "2.0.0"
description = "Professional database credentials management with security and team collaboration in mind"
readme = "README.md"
authors = [
    {name = "Your Company", email = "dev@yourcompany.com"}
]
license = {text = "MIT"}
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Database",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Operating System :: OS Independent",
]
requires-python = ">=3.8"
dependencies = [
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "typer[all]>=0.9.0",
    "rich>=13.0.0",
    "loguru>=0.7.0",
    "keyring>=24.0.0",
    "psycopg2-binary>=2.9.0",
    "sqlalchemy>=2.0.0",
    "python-multipart>=0.0.6",
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "jinja2>=3.1.0",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "aiofiles>=23.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.11.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.5.0",
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.0.0",
    "mkdocstrings[python]>=0.23.0",
]
mysql = ["mysqlclient>=2.2.0"]
oracle = ["oracledb>=1.4.0"]
mssql = ["pyodbc>=5.0.0"]

[project.scripts]
dbcreds = "dbcreds.cli:app"
dbcreds-server = "dbcreds.web.__main__:main"
dbcreds-migrate = "dbcreds.migrate:app"

[project.urls]
Homepage = "https://github.com/yourcompany/dbcreds"
Documentation = "https://yourcompany.github.io/dbcreds"
Repository = "https://github.com/yourcompany/dbcreds"
Issues = "https://github.com/yourcompany/dbcreds/issues"

[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
packages = ["dbcreds", "dbcreds.backends", "dbcreds.core", "dbcreds.web", "dbcreds.utils"]

[tool.ruff]
line-length = 120
target-version = "py38"

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"

# uv configuration
[tool.uv]
managed = true
dev-dependencies = [
    "ipython>=8.12.0",
    "ipdb>=0.13.13",
]
```

# Project Documentation

# dbcreds

Professional database credentials management with security and team collaboration in mind.

## Features

- 🔐 **Secure Storage**: Multiple backend support (Windows Credential Manager, macOS Keychain, Linux Secret Service)
- 🌍 **Multi-Environment**: Manage credentials for development, staging, and production
- 🚀 **Rich CLI**: Beautiful command-line interface with Rich and Typer
- 🌐 **Web UI**: Optional FastAPI web interface with HTMX
- 📊 **Multi-Database**: Support for PostgreSQL, MySQL, Oracle, SQL Server
- 🔄 **Password Rotation**: Track password age and expiration
- 📝 **Full Documentation**: Comprehensive docs with mkdocstrings
- 🎯 **Type Safety**: Pydantic models for validation

## Installation

Install directly from GitHub using pip:

```bash
pip install git+https://github.com/yourcompany/dbcreds.git
```

Or using uv:

```bash
uv pip install git+https://github.com/yourcompany/dbcreds.git
```

For development with additional database support:

```bash
# PostgreSQL only (default)
pip install git+https://github.com/yourcompany/dbcreds.git

# With MySQL support
pip install "git+https://github.com/yourcompany/dbcreds.git#egg=dbcreds[mysql]"

# With all databases
pip install "git+https://github.com/yourcompany/dbcreds.git#egg=dbcreds[mysql,oracle,mssql]"
```

## Quick Start

### 1. Initialize dbcreds

```bash
dbcreds init
```

### 2. Add credentials

```bash
# Add development database
dbcreds add dev --type postgresql
# Interactive prompts for connection details

# Add production database
dbcreds add prod --type postgresql --server prod.db.com --port 5432 --database myapp
# Password prompt appears
```

### 3. Use in Python

```python
from dbcreds import get_engine, get_connection

# Get SQLAlchemy engine
engine = get_engine("dev")

# Get connection
with get_connection("prod") as conn:
    df = pd.read_sql("SELECT * FROM users LIMIT 10", conn)

# Async support
from dbcreds import get_async_engine

async_engine = await get_async_engine("dev")
```

## CLI Usage

```bash
# List all environments
dbcreds list

# Show specific environment (without password)
dbcreds show dev

# Test connection
dbcreds test dev

# Update password
dbcreds update dev --password

# Remove environment
dbcreds remove dev

# Check password expiry
dbcreds check

# Export connection string
dbcreds export dev --format uri
```

## Web Interface

Start the web interface for team credential management:

```bash
dbcreds-server
# Visit http://localhost:8000
```

## Configuration

dbcreds stores configuration in `~/.dbcreds/config.json` and credentials in your system's secure storage.

## Development

```bash
# Clone the repository
git clone https://github.com/yourcompany/dbcreds.git
cd dbcreds

# Create virtual environment with uv
uv venv
uv pip install -e ".[dev]"

# Run tests
pytest

# Build documentation
mkdocs serve
```

## Security

- Credentials are never stored in plain text
- Each environment has isolated credentials
- Password rotation reminders
- Audit logging for credential access
- Team-based access control in web UI

## License

MIT License - see LICENSE file for details.


## Core Modules


```python # dbcreds/__init__.py
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
```

```python # dbcreds/core/__init__.py
# dbcreds/core/__init__.py
"""Core functionality for dbcreds."""

from dbcreds.core.manager import CredentialManager
from dbcreds.core.models import DatabaseCredentials, DatabaseType, Environment

__all__ = ["CredentialManager", "DatabaseCredentials", "DatabaseType", "Environment"]


```

```python # dbcreds/core/models.py
# dbcreds/core/models.py
"""
Pydantic models for database credentials.

This module defines the data models used throughout dbcreds for type safety
and validation.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, SecretStr, field_validator


class DatabaseType(str, Enum):
    """Supported database types."""

    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    ORACLE = "oracle"
    MSSQL = "mssql"
    SQLITE = "sqlite"


class Environment(BaseModel):
    """
    Database environment configuration.

    Represents a named database environment (e.g., dev, staging, prod) with
    its associated settings.

    Attributes:
        name: Environment name (e.g., 'dev', 'prod')
        database_type: Type of database
        description: Optional description of the environment
        is_production: Whether this is a production environment
        created_at: When the environment was created
        updated_at: When the environment was last updated
    """

    name: str = Field(..., min_length=1, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")
    database_type: DatabaseType
    description: Optional[str] = None
    is_production: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate environment name."""
        return v.lower()


class DatabaseCredentials(BaseModel):
    """
    Database connection credentials.

    Secure storage model for database connection information.

    Attributes:
        environment: Environment name
        host: Database server hostname or IP
        port: Database server port
        database: Database name
        username: Database username
        password: Database password (stored securely)
        options: Additional connection options
        ssl_mode: SSL connection mode
        password_updated_at: When the password was last updated
        password_expires_at: When the password expires
    """

    environment: str
    host: str
    port: int = Field(..., gt=0, le=65535)
    database: str
    username: str
    password: SecretStr
    options: Dict[str, Any] = Field(default_factory=dict)
    ssl_mode: Optional[str] = None
    password_updated_at: datetime = Field(default_factory=datetime.utcnow)
    password_expires_at: Optional[datetime] = None

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int, info) -> int:
        """Set default port based on database type if not specified."""
        if v is None and hasattr(info, "context") and "database_type" in info.context:
            db_type = info.context["database_type"]
            defaults = {
                DatabaseType.POSTGRESQL: 5432,
                DatabaseType.MYSQL: 3306,
                DatabaseType.ORACLE: 1521,
                DatabaseType.MSSQL: 1433,
            }
            return defaults.get(db_type, v)
        return v

    def get_connection_string(self, include_password: bool = True, driver: Optional[str] = None) -> str:
        """
        Generate a connection string for the database.

        Args:
            include_password: Whether to include the password in the connection string
            driver: Optional driver override for the connection string

        Returns:
            Database connection URI

        Examples:
            >>> creds.get_connection_string()
            'postgresql://user:pass@localhost:5432/mydb'
            >>> creds.get_connection_string(include_password=False)
            'postgresql://user@localhost:5432/mydb'
        """
        # This would be implemented based on database type
        # For now, return a PostgreSQL example
        password_part = f":{self.password.get_secret_value()}" if include_password else ""
        return f"postgresql://{self.username}{password_part}@{self.host}:{self.port}/{self.database}"

    def is_password_expired(self) -> bool:
        """Check if the password has expired."""
        if self.password_expires_at is None:
            return False
        return datetime.utcnow() > self.password_expires_at

    def days_until_expiry(self) -> Optional[int]:
        """Get the number of days until password expiry."""
        if self.password_expires_at is None:
            return None
        delta = self.password_expires_at - datetime.utcnow()
        return max(0, delta.days)  # Return 0 if already expired


class CredentialMetadata(BaseModel):
    """
    Metadata about stored credentials.

    Tracks additional information about credentials for management purposes.

    Attributes:
        environment: Environment name
        created_by: User who created the credentials
        created_at: When the credentials were created
        last_accessed: When the credentials were last accessed
        access_count: Number of times accessed
        last_tested: When the connection was last tested
        last_test_success: Whether the last test was successful
    """

    environment: str
    created_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_accessed: Optional[datetime] = None
    access_count: int = 0
    last_tested: Optional[datetime] = None
    last_test_success: Optional[bool] = None

```

```python # dbcreds/core/manager.py
# dbcreds/core/manager.py
"""
Core credential manager implementation.

This module provides the main CredentialManager class that orchestrates
credential storage and retrieval across different backends.
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Type

from loguru import logger
from pydantic import ValidationError

from dbcreds.backends.base import CredentialBackend
from dbcreds.backends.config import ConfigFileBackend
from dbcreds.backends.environment import EnvironmentBackend
from dbcreds.backends.keyring import KeyringBackend
from dbcreds.core.exceptions import (
    CredentialError,
    CredentialNotFoundError,
    PasswordExpiredError,
)
from dbcreds.core.models import DatabaseCredentials, DatabaseType, Environment

# Conditional import for Windows
if os.name == "nt":
    from dbcreds.backends.windows import WindowsCredentialBackend
    from dbcreds.backends.legacy_windows import LegacyWindowsBackend


class CredentialManager:
    """
    Main credential management class.

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

    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize the credential manager.

        Args:
            config_dir: Optional custom configuration directory. Defaults to ~/.dbcreds
        """
        self.config_dir = config_dir or os.path.expanduser("~/.dbcreds")
        os.makedirs(self.config_dir, exist_ok=True)

        self.backends: List[CredentialBackend] = []
        self.environments: Dict[str, Environment] = {}

        self._initialize_backends()
        self._load_environments()

        logger.debug(f"Initialized CredentialManager with {len(self.backends)} backends")

    def _initialize_backends(self) -> None:
        """Initialize available credential backends in priority order."""
        backend_classes: List[Type[CredentialBackend]] = []

        # Platform-specific backends first
        if os.name == "nt":
            backend_classes.append(WindowsCredentialBackend)
            # Add legacy backend for existing PowerShell credentials
            backend_classes.append(LegacyWindowsBackend)

        # Cross-platform backends
        backend_classes.extend([KeyringBackend, EnvironmentBackend, ConfigFileBackend])

        for backend_class in backend_classes:
            try:
                backend = backend_class()
                if backend.is_available():
                    self.backends.append(backend)
                    logger.debug(f"Initialized backend: {backend.__class__.__name__}")
            except Exception as e:
                logger.debug(f"Failed to initialize {backend_class.__name__}: {e}")

        if not self.backends:
            logger.warning("No credential backends available, falling back to config file only")
            self.backends.append(ConfigFileBackend(self.config_dir))

    def _load_environments(self) -> None:
        """Load environment configurations from disk."""
        config_backend = ConfigFileBackend(self.config_dir)
        environments_data = config_backend.load_environments()

        for env_data in environments_data:
            try:
                env = Environment(**env_data)
                self.environments[env.name] = env
            except ValidationError as e:
                logger.error(f"Invalid environment data: {e}")

    def add_environment(
        self,
        name: str,
        database_type: DatabaseType,
        description: Optional[str] = None,
        is_production: bool = False,
    ) -> Environment:
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

        logger.info(f"Added environment: {env.name}")
        return env

    def remove_environment(self, name: str) -> None:
        """
        Remove an environment and its credentials.

        Args:
            name: Environment name to remove

        Raises:
            CredentialNotFoundError: If environment doesn't exist
        """
        env_name = name.lower()
        if env_name not in self.environments:
            raise CredentialNotFoundError(f"Environment '{name}' not found")

        # Remove credentials from all backends
        for backend in self.backends:
            try:
                backend.delete_credential(f"dbcreds:{env_name}")
            except Exception as e:
                logger.debug(f"Failed to delete from {backend.__class__.__name__}: {e}")

        del self.environments[env_name]
        self._save_environments()

        logger.info(f"Removed environment: {env_name}")

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
    ) -> DatabaseCredentials:
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
        env_name = environment.lower()
        if env_name not in self.environments:
            raise CredentialNotFoundError(f"Environment '{environment}' not found")

        env = self.environments[env_name]

        # Calculate password expiration
        password_expires_at = None
        if password_expires_days:
            password_expires_at = datetime.utcnow() + timedelta(days=password_expires_days)

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
                if backend.set_credential(f"dbcreds:{env_name}", username, password, creds.model_dump()):
                    stored = True
                    logger.debug(f"Stored credentials in {backend.__class__.__name__}")
            except Exception as e:
                logger.debug(f"Failed to store in {backend.__class__.__name__}: {e}")

        if not stored:
            raise CredentialError("Failed to store credentials in any backend")

        logger.info(f"Stored credentials for environment: {env_name}")
        return creds

    def get_credentials(self, environment: str, check_expiry: bool = True) -> DatabaseCredentials:
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

                    logger.debug(f"Retrieved credentials from {backend.__class__.__name__}")
                    return creds
            except Exception as e:
                logger.debug(f"Failed to get from {backend.__class__.__name__}: {e}")

        raise CredentialNotFoundError(f"No credentials found for environment '{environment}'")

    def list_environments(self) -> List[Environment]:
        """
        List all configured environments.

        Returns:
            List of Environment objects

        Examples:
            >>> envs = manager.list_environments()
            >>> for env in envs:
            ...     print(env.name, env.database_type)
        """
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
            logger.error(f"Connection test failed for '{environment}': {e}")
            return False

    def _save_environments(self) -> None:
        """Save environment configurations to disk."""
        config_backend = ConfigFileBackend(self.config_dir)
        config_backend.save_environments([env.model_dump() for env in self.environments.values()])
```

```python # dbcreds/core/exceptions.py
# dbcreds/core/exceptions.py
"""
Custom exceptions for dbcreds.

This module defines all custom exceptions used throughout the package.
"""


class CredentialError(Exception):
    """Base exception for all credential-related errors."""

    pass


class CredentialNotFoundError(CredentialError):
    """Raised when requested credentials are not found."""

    pass


class PasswordExpiredError(CredentialError):
    """Raised when a password has expired."""

    pass


class BackendError(CredentialError):
    """Raised when a backend operation fails."""

    pass


class ValidationError(CredentialError):
    """Raised when credential validation fails."""

    pass
```


## Backend Implementations


```python # dbcreds/backends/base.py
# dbcreds/backends/base.py
"""
Base class for credential backends.

This module defines the abstract interface that all credential storage
backends must implement.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple


class CredentialBackend(ABC):
    """
    Abstract base class for credential storage backends.

    All credential backends must inherit from this class and implement
    the required methods.
    """

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if this backend is available on the current system.

        Returns:
            True if the backend can be used, False otherwise

        Examples:
            >>> backend = KeyringBackend()
            >>> if backend.is_available():
            ...     print("Keyring is available")
        """
        pass

    @abstractmethod
    def get_credential(self, key: str) -> Optional[Tuple[str, str, Dict[str, Any]]]:
        """
        Retrieve a credential from storage.

        Args:
            key: Unique identifier for the credential

        Returns:
            Tuple of (username, password, metadata) if found, None otherwise

        Examples:
            >>> result = backend.get_credential("dbcreds:dev")
            >>> if result:
            ...     username, password, metadata = result
        """
        pass

    @abstractmethod
    def set_credential(self, key: str, username: str, password: str, metadata: Dict[str, Any]) -> bool:
        """
        Store a credential.

        Args:
            key: Unique identifier for the credential
            username: Username to store
            password: Password to store
            metadata: Additional metadata to store

        Returns:
            True if successful, False otherwise

        Examples:
            >>> success = backend.set_credential(
            ...     "dbcreds:dev",
            ...     "myuser",
            ...     "mypass",
            ...     {"host": "localhost", "port": 5432}
            ... )
        """
        pass

    @abstractmethod
    def delete_credential(self, key: str) -> bool:
        """
        Delete a credential from storage.

        Args:
            key: Unique identifier for the credential

        Returns:
            True if successful, False otherwise

        Examples:
            >>> backend.delete_credential("dbcreds:dev")
        """
        pass

    def list_credentials(self) -> list[str]:
        """
        List all credential keys managed by this backend.

        Returns:
            List of credential keys

        Note:
            This is optional and may not be implemented by all backends.
        """
        return []
```

```python # dbcreds/backends/config.py
# dbcreds/backends/config.py
"""
JSON configuration file backend.

This backend stores non-sensitive configuration in JSON files and can
be used as a fallback or for storing metadata.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger

from dbcreds.backends.base import CredentialBackend


class ConfigFileBackend(CredentialBackend):
    """
    Configuration file backend.

    Stores environment configurations and non-sensitive metadata in JSON files.
    This backend should not be used for storing passwords directly.
    """

    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize the config file backend.

        Args:
            config_dir: Directory to store configuration files
        """
        self.config_dir = Path(config_dir or os.path.expanduser("~/.dbcreds"))
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.environments_file = self.config_dir / "environments.json"
        self.metadata_file = self.config_dir / "metadata.json"

    def is_available(self) -> bool:
        """Check if we can write to the config directory."""
        try:
            test_file = self.config_dir / ".test"
            test_file.touch()
            test_file.unlink()
            return True
        except Exception as e:
            logger.debug(f"Config directory not writable: {e}")
            return False

    def get_credential(self, key: str) -> Optional[Tuple[str, str, Dict[str, Any]]]:
        """
        Retrieve credential metadata from config file.

        Note: This backend does not store passwords.
        """
        metadata = self._load_metadata()
        if key in metadata:
            data = metadata[key]
            username = data.pop("username", "")
            # Password is not stored in config files
            return (username, "", data)
        return None

    def set_credential(self, key: str, username: str, password: str, metadata: Dict[str, Any]) -> bool:
        """
        Store credential metadata in config file.

        Note: Password is not stored, only metadata.
        """
        all_metadata = self._load_metadata()
        all_metadata[key] = {"username": username, **metadata}
        # Remove password if accidentally included in metadata
        all_metadata[key].pop("password", None)
        return self._save_metadata(all_metadata)

    def delete_credential(self, key: str) -> bool:
        """Delete credential metadata from config file."""
        metadata = self._load_metadata()
        if key in metadata:
            del metadata[key]
            return self._save_metadata(metadata)
        return True

    def load_environments(self) -> List[Dict[str, Any]]:
        """Load environment configurations."""
        if self.environments_file.exists():
            try:
                with open(self.environments_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load environments: {e}")
        return []

    def save_environments(self, environments: List[Dict[str, Any]]) -> bool:
        """Save environment configurations."""
        try:
            with open(self.environments_file, "w") as f:
                json.dump(environments, f, indent=2, default=str)
            return True
        except Exception as e:
            logger.error(f"Failed to save environments: {e}")
            return False

    def _load_metadata(self) -> Dict[str, Dict[str, Any]]:
        """Load metadata from file."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load metadata: {e}")
        return {}

    def _save_metadata(self, metadata: Dict[str, Dict[str, Any]]) -> bool:
        """Save metadata to file."""
        try:
            with open(self.metadata_file, "w") as f:
                json.dump(metadata, f, indent=2, default=str)
            return True
        except Exception as e:
            logger.error(f"Failed to save metadata: {e}")
            return False

```

```python # dbcreds/backends/windows.py
# dbcreds/backends/windows.py
"""
Windows Credential Manager backend.

This backend provides secure credential storage using Windows Credential Manager
through the Windows API.
"""

import ctypes
import ctypes.wintypes
import json
import sys
from typing import Any, Dict, Optional, Tuple

from loguru import logger

from dbcreds.backends.base import CredentialBackend


class CREDENTIAL(ctypes.Structure):
    """Windows CREDENTIAL structure."""

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


class WindowsCredentialBackend(CredentialBackend):
    """
    Windows Credential Manager backend.

    Uses the Windows API to securely store credentials in the Windows
    Credential Manager.
    """

    CRED_TYPE_GENERIC = 1
    CRED_PERSIST_LOCAL_MACHINE = 2

    def __init__(self):
        """Initialize Windows API functions."""
        if sys.platform != "win32":
            raise RuntimeError("Windows Credential Manager is only available on Windows")

        self.advapi32 = ctypes.windll.advapi32

        # CredReadW
        self.advapi32.CredReadW.argtypes = [
            ctypes.wintypes.LPCWSTR,
            ctypes.wintypes.DWORD,
            ctypes.wintypes.DWORD,
            ctypes.POINTER(ctypes.POINTER(CREDENTIAL)),
        ]
        self.advapi32.CredReadW.restype = ctypes.wintypes.BOOL

        # CredWriteW
        self.advapi32.CredWriteW.argtypes = [ctypes.POINTER(CREDENTIAL), ctypes.wintypes.DWORD]
        self.advapi32.CredWriteW.restype = ctypes.wintypes.BOOL

        # CredDeleteW
        self.advapi32.CredDeleteW.argtypes = [
            ctypes.wintypes.LPCWSTR,
            ctypes.wintypes.DWORD,
            ctypes.wintypes.DWORD,
        ]
        self.advapi32.CredDeleteW.restype = ctypes.wintypes.BOOL

        # CredFree
        self.advapi32.CredFree.argtypes = [ctypes.c_void_p]

    def is_available(self) -> bool:
        """Check if Windows Credential Manager is available."""
        return sys.platform == "win32"

    def get_credential(self, key: str) -> Optional[Tuple[str, str, Dict[str, Any]]]:
        """Retrieve credential from Windows Credential Manager."""
        cred_ptr = ctypes.POINTER(CREDENTIAL)()

        success = self.advapi32.CredReadW(key, self.CRED_TYPE_GENERIC, 0, ctypes.byref(cred_ptr))

        if not success:
            return None

        try:
            cred = cred_ptr.contents
            username = cred.UserName if cred.UserName else ""

            # Extract credential blob
            blob_size = cred.CredentialBlobSize
            if blob_size > 0:
                # Credential blob contains JSON with password and metadata
                blob_data = ctypes.string_at(cred.CredentialBlob, blob_size)
                blob_str = blob_data.decode("utf-16le", errors="ignore").rstrip("\x00")

                try:
                    data = json.loads(blob_str)
                    password = data.pop("password", "")
                    return (username, password, data)
                except json.JSONDecodeError:
                    # Fallback for old format (password only)
                    return (username, blob_str, {})
            else:
                return (username, "", {})
        finally:
            self.advapi32.CredFree(cred_ptr)

    def set_credential(self, key: str, username: str, password: str, metadata: Dict[str, Any]) -> bool:
        """Store credential in Windows Credential Manager."""
        # First delete any existing credential
        self.delete_credential(key)

        # Prepare credential data as JSON
        data = {"password": password, **metadata}
        blob_str = json.dumps(data)
        blob_bytes = blob_str.encode("utf-16le")

        # Create credential structure
        cred = CREDENTIAL()
        cred.Type = self.CRED_TYPE_GENERIC
        cred.Persist = self.CRED_PERSIST_LOCAL_MACHINE
        cred.TargetName = ctypes.c_wchar_p(key)
        cred.UserName = ctypes.c_wchar_p(username)
        cred.CredentialBlobSize = len(blob_bytes)
        cred.CredentialBlob = ctypes.cast(
            ctypes.create_string_buffer(blob_bytes), ctypes.POINTER(ctypes.c_char)
        )

        success = self.advapi32.CredWriteW(ctypes.byref(cred), 0)
        return bool(success)

    def delete_credential(self, key: str) -> bool:
        """Delete credential from Windows Credential Manager."""
        success = self.advapi32.CredDeleteW(key, self.CRED_TYPE_GENERIC, 0)
        return bool(success)

```

```python # dbcreds/backends/keyring.py
# dbcreds/backends/keyring.py
"""
Cross-platform keyring backend using python-keyring.

This backend provides secure credential storage using the system's
native credential store (Keychain on macOS, Credential Manager on Windows,
Secret Service on Linux).
"""

import json
from typing import Any, Dict, Optional, Tuple

import keyring
from keyring.errors import KeyringError
from loguru import logger

from dbcreds.backends.base import CredentialBackend


class KeyringBackend(CredentialBackend):
    """
    Keyring-based credential storage backend.

    Uses the python-keyring library to store credentials in the system's
    native credential store.
    """

    SERVICE_NAME = "dbcreds"

    def is_available(self) -> bool:
        """Check if keyring is available and functional."""
        try:
            # Test keyring by trying to get a non-existent key
            keyring.get_password(self.SERVICE_NAME, "test_availability")
            return True
        except Exception as e:
            logger.debug(f"Keyring not available: {e}")
            return False

    def get_credential(self, key: str) -> Optional[Tuple[str, str, Dict[str, Any]]]:
        """Retrieve credential from keyring."""
        try:
            # Get the stored data
            stored_data = keyring.get_password(self.SERVICE_NAME, key)
            if not stored_data:
                return None

            # Parse the JSON data
            data = json.loads(stored_data)
            username = data.pop("username", "")
            password = data.pop("password", "")

            return (username, password, data)
        except (KeyringError, json.JSONDecodeError) as e:
            logger.error(f"Failed to retrieve credential from keyring: {e}")
            return None

    def set_credential(self, key: str, username: str, password: str, metadata: Dict[str, Any]) -> bool:
        """Store credential in keyring."""
        try:
            # Combine all data into a single JSON object
            data = {"username": username, "password": password, **metadata}
            stored_data = json.dumps(data)

            # Store in keyring
            keyring.set_password(self.SERVICE_NAME, key, stored_data)
            return True
        except (KeyringError, json.JSONEncodeError) as e:
            logger.error(f"Failed to store credential in keyring: {e}")
            return False

    def delete_credential(self, key: str) -> bool:
        """Delete credential from keyring."""
        try:
            keyring.delete_password(self.SERVICE_NAME, key)
            return True
        except KeyringError as e:
            logger.error(f"Failed to delete credential from keyring: {e}")
            return False

    def list_credentials(self) -> list[str]:
        """List all dbcreds keys in keyring."""
        # Note: python-keyring doesn't provide a way to list all keys
        # This would need to be tracked separately
        return []

```

```python # dbcreds/backends/environment.py
# dbcreds/backends/environment.py
"""
Environment variable backend for credential storage.

This backend reads credentials from environment variables, useful for
containerized deployments and CI/CD pipelines.
"""

import os
from typing import Any, Dict, Optional, Tuple

from loguru import logger

from dbcreds.backends.base import CredentialBackend


class EnvironmentBackend(CredentialBackend):
    """
    Environment variable credential backend.

    Reads credentials from environment variables using a naming convention.
    Variables should be named as: DBCREDS_{ENV}_{FIELD}

    Example:
        DBCREDS_DEV_HOST=localhost
        DBCREDS_DEV_PORT=5432
        DBCREDS_DEV_USERNAME=myuser
        DBCREDS_DEV_PASSWORD=mypass
    """

    def is_available(self) -> bool:
        """Environment variables are always available."""
        return True

    def get_credential(self, key: str) -> Optional[Tuple[str, str, Dict[str, Any]]]:
        """Retrieve credential from environment variables."""
        # Extract environment name from key (e.g., "dbcreds:dev" -> "dev")
        if not key.startswith("dbcreds:"):
            return None

        env_name = key.split(":", 1)[1].upper()
        prefix = f"DBCREDS_{env_name}_"

        # Look for environment variables with this prefix
        metadata = {}
        username = None
        password = None

        for var_name, value in os.environ.items():
            if var_name.startswith(prefix):
                field_name = var_name[len(prefix) :].lower()
                if field_name == "username":
                    username = value
                elif field_name == "password":
                    password = value
                else:
                    # Try to convert to appropriate type
                    if field_name == "port":
                        try:
                            metadata[field_name] = int(value)
                        except ValueError:
                            metadata[field_name] = value
                    else:
                        metadata[field_name] = value

        if username and password:
            logger.debug(f"Found credentials in environment for {key}")
            return (username, password, metadata)

        return None

    def set_credential(self, key: str, username: str, password: str, metadata: Dict[str, Any]) -> bool:
        """
        Set credential in environment variables.

        Note: This only affects the current process and its children.
        """
        if not key.startswith("dbcreds:"):
            return False

        env_name = key.split(":", 1)[1].upper()
        prefix = f"DBCREDS_{env_name}_"

        # Set environment variables
        os.environ[f"{prefix}USERNAME"] = username
        os.environ[f"{prefix}PASSWORD"] = password

        for field, value in metadata.items():
            os.environ[f"{prefix}{field.upper()}"] = str(value)

        return True

    def delete_credential(self, key: str) -> bool:
        """Delete credential from environment variables."""
        if not key.startswith("dbcreds:"):
            return False

        env_name = key.split(":", 1)[1].upper()
        prefix = f"DBCREDS_{env_name}_"

        # Remove all variables with this prefix
        vars_to_remove = [var for var in os.environ if var.startswith(prefix)]
        for var in vars_to_remove:
            os.environ.pop(var, None)

        return True
```

```python # dbcreds/backends/legacy_windows.py
# dbcreds/backends/legacy_windows.py
"""
Legacy Windows Credential Manager backend for existing credentials.

This backend reads credentials stored in the format used by the PowerShell profile.
"""

import ctypes
import json
import os
from typing import Any, Dict, Optional, Tuple

from loguru import logger

from dbcreds.backends.windows import CREDENTIAL, WindowsCredentialBackend
from dbcreds.core.models import DatabaseType


class LegacyWindowsBackend(WindowsCredentialBackend):
    """
    Backend for reading legacy Windows credentials stored by PowerShell profile.
    
    Reads credentials stored as:
    - Target: DBCredentials:{database_name}
    - Environment variables: DB_SERVER, DB_PORT, DB_NAME, DB_USER
    - JSON config at ~/.db_credentials/config.json
    """
    
    def __init__(self):
        """Initialize the legacy backend."""
        super().__init__()
        self.config_path = os.path.expanduser("~/.db_credentials/config.json")
    
    def get_credential(self, key: str) -> Optional[Tuple[str, str, Dict[str, Any]]]:
        """
        Retrieve credential from legacy storage.
        
        First tries dbcreds format, then falls back to legacy format.
        """
        # Try standard dbcreds format first
        result = super().get_credential(key)
        if result:
            return result
        
        # Extract environment name from key (e.g., "dbcreds:dev" -> "dev")
        if not key.startswith("dbcreds:"):
            return None
        
        env_name = key.split(":", 1)[1]
        
        # Try to find legacy credentials
        return self._get_legacy_credential(env_name)
    
    def _get_legacy_credential(self, env_name: str) -> Optional[Tuple[str, str, Dict[str, Any]]]:
        """Get credential from legacy PowerShell storage."""
        # First check if there's a JSON config file
        config = self._load_legacy_config()
        
        if config:
            # Try to get password from Windows Credential Manager using legacy format
            legacy_target = f"DBCredentials:{config.get('database', '')}"
            password = None
            
            try:
                password = self._get_password_from_legacy_target(legacy_target)
            except Exception as e:
                logger.debug(f"Could not get password from legacy target: {e}")
            
            if password:
                username = config.get("username", "")
                metadata = {
                    "host": config.get("server", "localhost"),
                    "port": int(config.get("port", 5432)),
                    "database": config.get("database", ""),
                    "password_updated_at": config.get("update_date", ""),
                    "password_expires_days": config.get("expiry_days", 90),
                }
                
                return (username, password, metadata)
        
        # Fall back to environment variables
        if all(os.environ.get(var) for var in ["DB_SERVER", "DB_PORT", "DB_NAME", "DB_USER"]):
            username = os.environ.get("DB_USER", "")
            password = os.environ.get("DB_PWD", "")
            
            # If no password in env, try legacy credential manager format
            if not password:
                db_name = os.environ.get("DB_NAME", "")
                legacy_target = f"DBCredentials:{db_name}"
                try:
                    password = self._get_password_from_legacy_target(legacy_target)
                except:
                    pass
            
            if password:
                metadata = {
                    "host": os.environ.get("DB_SERVER", "localhost"),
                    "port": int(os.environ.get("DB_PORT", 5432)),
                    "database": os.environ.get("DB_NAME", ""),
                    "password_updated_at": os.environ.get("DB_PWD_DATE", ""),
                    "password_expires_days": int(os.environ.get("DB_PWD_EXPIRY", 90)),
                }
                
                return (username, password, metadata)
        
        return None
    
    def _get_password_from_legacy_target(self, target: str) -> Optional[str]:
        """Get password using legacy target format."""
        cred_ptr = ctypes.POINTER(CREDENTIAL)()
        
        success = self.advapi32.CredReadW(
            target, 
            self.CRED_TYPE_GENERIC, 
            0, 
            ctypes.byref(cred_ptr)
        )
        
        if not success:
            return None
        
        try:
            cred = cred_ptr.contents
            
            # Extract password from credential blob
            blob_size = cred.CredentialBlobSize
            if blob_size > 0:
                blob_data = ctypes.string_at(cred.CredentialBlob, blob_size)
                # Legacy format stores password as UTF-16LE
                password = blob_data.decode("utf-16le", errors="ignore").rstrip("\x00")
                return password
            
            return None
        finally:
            self.advapi32.CredFree(cred_ptr)
    
    def _load_legacy_config(self) -> Optional[Dict[str, Any]]:
        """Load legacy configuration from JSON file."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.debug(f"Could not load legacy config: {e}")
        
        return None
```


## Web Interface


```python # dbcreds/web/__init__.py
# dbcreds/web/__init__.py
"""Web interface for dbcreds using FastAPI and HTMX."""


```

```python # dbcreds/web/__main__.py
# dbcreds/web/__main__.py
"""Entry point for dbcreds-server command."""

import sys

import typer
from rich.console import Console

from dbcreds.web.main import run_server

console = Console()


def main():
    """Run the dbcreds web server."""
    try:
        run_server()
    except KeyboardInterrupt:
        console.print("\n[yellow]Server stopped by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]Failed to start server:[/bold red] {e}")
        console.print_exception()
        sys.exit(1)


if __name__ == "__main__":
    main()
```

```python # dbcreds/web/main.py
# dbcreds/web/main.py
"""
FastAPI web application for dbcreds.

Provides a web interface for managing database credentials with
team collaboration features.
"""

import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
from rich.console import Console
from rich.panel import Panel  # Add this import
from rich.traceback import install as install_rich_traceback

from dbcreds import __version__
from dbcreds.core.exceptions import CredentialError
from dbcreds.core.manager import CredentialManager
from dbcreds.web.errors import web_error_handler
from datetime import datetime
from dbcreds.core.models import DatabaseType
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
# Install rich traceback handler
install_rich_traceback(show_locals=True)

# Create console for startup messages
console = Console()

# Create FastAPI app
app = FastAPI(
    title="dbcreds Web",
    description="Database Credentials Management",
    version=__version__,
)
# Add after app creation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # Configure for production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1"],  # Configure for production
)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
# Setup templates
templates_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# Mount static files
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


# Exception handlers
@app.exception_handler(CredentialError)
async def credential_error_handler(request: Request, exc: CredentialError):
    """Handle credential errors."""
    return web_error_handler.get_error_response(request, exc)


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions."""
    return web_error_handler.get_error_response(request, exc)


@app.exception_handler(HTTPException)
async def http_exception_handler_custom(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    # Log HTTP exceptions with rich formatting
    web_error_handler.log_error(exc, request)
    return await http_exception_handler(request, exc)


@app.on_event("startup")
async def startup_event():
    """Run on startup."""
    console.print(Panel.fit(
        f"[bold green]dbcreds Web Server v{__version__}[/bold green]\n"
        f"[dim]Ready to manage your database credentials[/dim]",
        title="Starting Up",
        border_style="green"
    ))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Home page."""
    try:
        manager = CredentialManager()
        environments = manager.list_environments()

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "title": "dbcreds",
                "environments": environments,
                "version": __version__,
            },
        )
    except Exception as e:
        # Errors will be caught by exception handlers
        raise


@app.get("/environments", response_class=HTMLResponse)
async def list_environments(request: Request):
    """List all environments (HTMX endpoint)."""
    try:
        manager = CredentialManager()
        environments = manager.list_environments()

        return templates.TemplateResponse(
            "partials/environment_list.html",
            {
                "request": request,
                "environments": environments,
            },
        )
    except Exception as e:
        # Log the actual error
        console.print(f"[red]Error loading environments:[/red] {e}")
        if os.getenv("DBCREDS_DEBUG"):
            console.print_exception()
        
        # For HTMX requests, return a simple error partial
        return HTMLResponse(
            content=f'<div class="text-red-600 p-4">Error loading environments: {str(e)}</div>',
            status_code=500
        )
@app.get("/settings", response_class=HTMLResponse)
async def settings(request: Request):
    """Settings page."""
    try:
        manager = CredentialManager()
        
        # Get backend information
        backends_info = []
        for backend in manager.backends:
            backend_name = backend.__class__.__name__
            backend_info = {
                "name": backend_name.replace("Backend", ""),
                "description": "",
                "available": backend.is_available()
            }
            
            # Add descriptions for known backends
            if "Keyring" in backend_name:
                backend_info["description"] = "System keyring (Keychain on macOS, Credential Manager on Windows)"
            elif "Windows" in backend_name:
                backend_info["description"] = "Windows Credential Manager"
            elif "Environment" in backend_name:
                backend_info["description"] = "Environment variables"
            elif "Config" in backend_name:
                backend_info["description"] = "JSON configuration files"
            
            backends_info.append(backend_info)

        return templates.TemplateResponse(
            "settings.html",
            {
                "request": request,
                "title": "Settings - dbcreds",
                "version": __version__,
                "config_dir": manager.config_dir,
                "backends": backends_info,
            },
        )
    except Exception as e:
        # Errors will be caught by exception handlers
        raise


@app.post("/environments", response_class=HTMLResponse)
async def create_environment(request: Request):
    """Create a new environment."""
    try:
        form_data = await request.form()
        manager = CredentialManager()
        
        # Add the environment
        env_name = form_data.get("name", "").lower()
        db_type = DatabaseType(form_data.get("database_type"))
        
        manager.add_environment(
            env_name,
            db_type,
            description=form_data.get("description", ""),
            is_production=bool(form_data.get("is_production", False))
        )
        
        # Set credentials
        manager.set_credentials(
            env_name,
            host=form_data.get("host"),
            port=int(form_data.get("port", 5432)),
            database=form_data.get("database"),
            username=form_data.get("username"),
            password=form_data.get("password"),
            password_expires_days=int(form_data.get("expires_days", 90))
        )
        
        # Return updated environment list
        environments = manager.list_environments()
        return templates.TemplateResponse(
            "partials/environment_list.html",
            {"request": request, "environments": environments},
        )
    except Exception as e:
        return HTMLResponse(
            content=f'<div class="text-red-600 p-4">Error: {str(e)}</div>',
            status_code=400
        )


@app.get("/environments/{env_name}/edit", response_class=HTMLResponse)
async def edit_environment_form(request: Request, env_name: str):
    """Get edit form for an environment."""
    try:
        manager = CredentialManager()
        creds = manager.get_credentials(env_name, check_expiry=False)
        env = next((e for e in manager.list_environments() if e.name == env_name), None)
        
        if not env:
            raise HTTPException(status_code=404, detail="Environment not found")
        
        # Calculate days until expiry
        days_left = creds.days_until_expiry()
        
        # Calculate the total expiry period (not the days left)
        expiry_period = 90  # Default
        if creds.password_expires_at and creds.password_updated_at:
            expiry_period = (creds.password_expires_at - creds.password_updated_at).days
        
        html = f"""
        <div class="fixed z-10 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
            <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
                <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
                <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
                    <div>
                        <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                            Edit Environment: {env_name}
                        </h3>
                        <div class="mt-2">
                            <form hx-put="/environments/{env_name}" hx-target="#environment-list" hx-swap="innerHTML">
                                <div class="space-y-4">
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700">
                                            Connection Details
                                        </label>
                                        <div class="mt-1 text-sm text-gray-500">
                                            Host: {creds.host}:{creds.port}<br>
                                            Database: {creds.database}<br>
                                            Username: {creds.username}<br>
                                            Type: {env.database_type.value}
                                        </div>
                                    </div>
                                    
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700">
                                            Password Status
                                        </label>
                                        <div class="mt-1 text-sm">
                                            {'''
                                            <span class="text-red-600">Expired</span>
                                            ''' if creds.is_password_expired() else f'''
                                            <span class="text-green-600">{days_left} days remaining</span>
                                            ''' if days_left is not None else '''
                                            <span class="text-gray-600">No expiry set</span>
                                            '''}
                                            <div class="text-xs text-gray-500 mt-1">
                                                Last updated: {creds.password_updated_at.strftime('%Y-%m-%d')}
                                                {f'''<br>Expires on: {creds.password_expires_at.strftime('%Y-%m-%d')}''' if creds.password_expires_at else ''}
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div>
                                        <label for="password" class="block text-sm font-medium text-gray-700">
                                            New Password (leave blank to keep current)
                                        </label>
                                        <input type="password" name="password" id="password"
                                               class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                                    </div>
                                    
                                    <div>
                                        <label for="password_updated_at" class="block text-sm font-medium text-gray-700">
                                            Password Last Updated Date
                                        </label>
                                        <input type="date" name="password_updated_at" id="password_updated_at"
                                               value="{creds.password_updated_at.strftime('%Y-%m-%d')}"
                                               class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                                        <p class="mt-1 text-xs text-gray-500">
                                            Use this to adjust when the password was last updated.
                                        </p>
                                    </div>
                                    
                                    <div>
                                        <label for="expires_days" class="block text-sm font-medium text-gray-700">
                                            Password Expiry (days)
                                        </label>
                                        <input type="number" name="expires_days" id="expires_days" 
                                               value="{expiry_period}"
                                               class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                                        <p class="mt-1 text-xs text-gray-500">
                                            Total days passwords are valid for (from update date).
                                        </p>
                                    </div>
                                </div>
                                
                                <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                                    <button type="submit"
                                            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:col-start-2 sm:text-sm">
                                        Update
                                    </button>
                                    <button type="button" onclick="document.getElementById('modal').innerHTML=''"
                                            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:col-start-1 sm:text-sm">
                                        Cancel
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        
        return HTMLResponse(content=html)
    except Exception as e:
        return HTMLResponse(
            content=f'<div class="text-red-600 p-4">Error: {str(e)}</div>',
            status_code=500
        )

@app.put("/environments/{env_name}", response_class=HTMLResponse)
async def update_environment(request: Request, env_name: str):
    """Update an environment."""
    try:
        form_data = await request.form()
        manager = CredentialManager()
        
        # Get existing credentials
        creds = manager.get_credentials(env_name, check_expiry=False)
        
        # Get the expires_days value
        expires_days = int(form_data.get("expires_days", 90))
        
        # Check if password updated date was changed
        new_update_date_str = form_data.get("password_updated_at", "").strip()
        password_updated_at = None
        if new_update_date_str:
            from datetime import datetime
            # Parse the date from the form
            try:
                password_updated_at = datetime.strptime(new_update_date_str, '%Y-%m-%d')
            except ValueError:
                return HTMLResponse(
                    content='<div class="text-red-600 p-4">Error: Invalid date format</div>',
                    status_code=400
                )
        
        # Update password or other fields if needed
        new_password = form_data.get("password", "").strip()
        # Always consider an update needed if expiry days are set
        update_needed = new_password or password_updated_at or expires_days > 0
        
        if update_needed:
            # We need to directly modify the credentials in the backend
            if not new_password:
                # If only changing the update date, reuse existing password
                new_password = creds.password.get_secret_value()
                
            # Use the existing update date if not provided
            if not password_updated_at:
                password_updated_at = creds.password_updated_at
            
            # Create a new credentials object with updated fields
            manager.set_credentials(
                env_name,
                host=creds.host,
                port=creds.port,
                database=creds.database,
                username=creds.username,
                password=new_password,
                # Always set the password_expires_days to ensure expiry is calculated
                password_expires_days=expires_days
            )
            
            # If we need to modify the update date, we need to access the backends
            if password_updated_at:
                # We need to update the password_updated_at field directly
                for backend in manager.backends:
                    if backend.is_available():
                        try:
                            # Get the raw credentials from the backend
                            result = backend.get_credential(f"dbcreds:{env_name}")
                            if result:
                                username, password, metadata = result
                                # Modify the password_updated_at field in metadata
                                metadata["password_updated_at"] = password_updated_at.isoformat()
                                # Always calculate the new expiry date
                                from datetime import timedelta
                                expires_at = password_updated_at + timedelta(days=expires_days)
                                metadata["password_expires_at"] = expires_at.isoformat()
                                # Save back to the backend using set_credential
                                backend.set_credential(f"dbcreds:{env_name}", username, password, metadata)
                                break
                        except Exception as backend_error:
                            logger.error(f"Error updating credentials in backend {backend.__class__.__name__}: {backend_error}")
                            continue
        
        # Clear modal and refresh list
        environments = manager.list_environments()
        return templates.TemplateResponse(
            "partials/environment_list.html",
            {"request": request, "environments": environments},
        )
    except Exception as e:
        return HTMLResponse(
            content=f'<div class="text-red-600 p-4">Error: {str(e)}</div>',
            status_code=400
        )

@app.post("/environments/{env_name}/test", response_class=HTMLResponse)
async def test_environment(request: Request, env_name: str):
    """Test environment connection."""
    try:
        manager = CredentialManager()
        success = manager.test_connection(env_name)
        
        if success:
            return HTMLResponse(
                content='<div class="text-green-600 p-4">✓ Connection successful!</div>'
            )
        else:
            return HTMLResponse(
                content='<div class="text-red-600 p-4">✗ Connection failed!</div>'
            )
    except Exception as e:
        return HTMLResponse(
            content=f'<div class="text-red-600 p-4">Error: {str(e)}</div>',
            status_code=500
        )


@app.get("/environments/new", response_class=HTMLResponse)
async def new_environment_form(request: Request):
    """New environment form (HTMX modal)."""
    from dbcreds.core.models import DatabaseType
    
    # Default ports for each database type
    default_ports = {
        DatabaseType.POSTGRESQL: 5432,
        DatabaseType.MYSQL: 3306,
        DatabaseType.MSSQL: 1433,
        DatabaseType.ORACLE: 1521,
    }
    
    return HTMLResponse(content=f"""
    <div class="fixed z-10 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
            <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
            <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
                <div>
                    <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                        Add New Environment
                    </h3>
                    <div class="mt-2">
                        <form hx-post="/environments" hx-target="#environment-list" hx-swap="innerHTML">
                            <div class="space-y-4">
                                <div>
                                    <label for="name" class="block text-sm font-medium text-gray-700">
                                        Environment Name
                                    </label>
                                    <input type="text" name="name" id="name" required
                                           class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                           placeholder="dev, staging, prod">
                                </div>
                                
                                <div>
                                    <label for="database_type" class="block text-sm font-medium text-gray-700">
                                        Database Type
                                    </label>
                                    <select name="database_type" id="database_type" required
                                            class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                                            onchange="updateDefaultPort(this.value)">
                                        {''.join(f'<option value="{dt.value}" data-port="{default_ports.get(dt, 5432)}">{dt.value.title()}</option>' for dt in DatabaseType)}
                                    </select>
                                </div>
                                
                                <div class="grid grid-cols-2 gap-4">
                                    <div>
                                        <label for="host" class="block text-sm font-medium text-gray-700">
                                            Server/Host
                                        </label>
                                        <input type="text" name="host" id="host" required
                                               class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                               placeholder="localhost">
                                    </div>
                                    
                                    <div>
                                        <label for="port" class="block text-sm font-medium text-gray-700">
                                            Port
                                        </label>
                                        <input type="number" name="port" id="port" required value="5432"
                                               class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                                    </div>
                                </div>
                                
                                <div>
                                    <label for="database" class="block text-sm font-medium text-gray-700">
                                        Database Name
                                    </label>
                                    <input type="text" name="database" id="database" required
                                           class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                           placeholder="mydb">
                                </div>
                                
                                <div>
                                    <label for="username" class="block text-sm font-medium text-gray-700">
                                        Username
                                    </label>
                                    <input type="text" name="username" id="username" required
                                           class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                                </div>
                                
                                <div>
                                    <label for="password" class="block text-sm font-medium text-gray-700">
                                        Password
                                    </label>
                                    <input type="password" name="password" id="password" required
                                           class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                                </div>
                                
                                <div>
                                    <label for="expires_days" class="block text-sm font-medium text-gray-700">
                                        Password Expiry (days)
                                    </label>
                                    <input type="number" name="expires_days" id="expires_days" value="90"
                                           class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                                </div>
                                
                                <div>
                                    <label for="description" class="block text-sm font-medium text-gray-700">
                                        Description
                                    </label>
                                    <input type="text" name="description" id="description"
                                           class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                           placeholder="Optional description">
                                </div>
                                
                                <div class="flex items-center">
                                    <input type="checkbox" name="is_production" id="is_production"
                                           class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded">
                                    <label for="is_production" class="ml-2 block text-sm text-gray-900">
                                        Production Environment
                                    </label>
                                </div>
                            </div>
                            
                            <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                                <button type="submit"
                                        class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:col-start-2 sm:text-sm">
                                    Add Environment
                                </button>
                                <button type="button" onclick="document.getElementById('modal').innerHTML=''"
                                        class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:col-start-1 sm:text-sm">
                                    Cancel
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script>
        function updateDefaultPort(dbType) {{
            const select = document.getElementById('database_type');
            const option = select.querySelector(`option[value="${{dbType}}"]`);
            const port = option.getAttribute('data-port');
            document.getElementById('port').value = port;
        }}
    </script>
    """)
@app.get("/api/environments/{env_name}/expiry")
async def get_environment_expiry(env_name: str):
    """Get password expiry information for an environment."""
    try:
        manager = CredentialManager()
        creds = manager.get_credentials(env_name, check_expiry=False)
        
        # Calculate days until expiry
        days_left = None
        expiry_days = 90  # Default value
        
        if creds.password_expires_at and creds.password_updated_at:
            # Calculate the total expiry period in days
            expiry_days = (creds.password_expires_at - creds.password_updated_at).days
            days_left = creds.days_until_expiry()
        elif creds.password_updated_at:
            # If we have updated_at but no expires_at, calculate it with default 90 days
            from datetime import timedelta, datetime
            expires_at = creds.password_updated_at + timedelta(days=expiry_days)
            delta = expires_at - datetime.utcnow()
            days_left = delta.days if delta.days > 0 else 0
        
        return {
            "days_left": days_left,
            "is_expired": creds.is_password_expired() if creds.password_expires_at else (days_left == 0 if days_left is not None else False),
            "expires_at": creds.password_expires_at.isoformat() if creds.password_expires_at else None,
            "updated_at": creds.password_updated_at.isoformat() if creds.password_updated_at else None,
            "has_expiry": creds.password_expires_at is not None or creds.password_updated_at is not None,
            "expires_days": expiry_days  # Total expiry window
        }
    except Exception as e:
        logger.error(f"Error getting expiry for {env_name}: {e}")
        return {"error": str(e), "days_left": None, "is_expired": False, "updated_at": None, "has_expiry": False}



def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """Run the web server."""
    console.print(f"\n[bold blue]Starting dbcreds web server[/bold blue]")
    console.print(f"[green]➜[/green] Local:   http://localhost:{port}")
    console.print(f"[green]➜[/green] Network: http://{host}:{port}\n")
    
    # Configure uvicorn with custom logging
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["default"]["fmt"] = "%(levelprefix)s %(message)s"
    log_config["formatters"]["access"]["fmt"] = '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
    
    uvicorn.run(
        "dbcreds.web.main:app" if reload else app,
        host=host,
        port=port,
        reload=reload,
        log_config=log_config,
    )


if __name__ == "__main__":
    run_server(reload=True)
```

```python # dbcreds/web/errors.py
# dbcreds/web/errors.py
"""Error handling for the web interface."""

import sys
import traceback
from typing import Optional

from fastapi import Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.traceback import Traceback

from dbcreds.core.exceptions import (
    BackendError,
    CredentialError,
    CredentialNotFoundError,
    PasswordExpiredError,
    ValidationError,
)


class WebErrorHandler:
    """Rich error handler for web interface."""
    
    def __init__(self):
        """Initialize with a console for stderr output."""
        self.console = Console(stderr=True, force_terminal=True)
    
    def log_error(self, error: Exception, request: Optional[Request] = None) -> None:
        """Log error with rich formatting to console."""
        # Create error panel
        error_text = Text()
        error_text.append(f"{error.__class__.__name__}: ", style="bold red")
        error_text.append(str(error), style="red")
        
        if request:
            error_text.append(f"\n\nRequest: {request.method} {request.url}", style="dim")
        
        panel = Panel(
            error_text,
            title="[bold red]Web Server Error[/bold red]",
            border_style="red",
            padding=(1, 2),
        )
        self.console.print(panel)
        
        # Print rich traceback if debug mode
        if logger._core.min_level <= 10:  # DEBUG level
            tb = Traceback.from_exception(
                type(error),
                error,
                error.__traceback__,
                show_locals=True,
                suppress=[sys.modules[__name__]],
            )
            self.console.print(tb)
    
    def get_error_response(
        self, 
        request: Request, 
        error: Exception,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    ) -> HTMLResponse:
        """Get HTML error response for the web interface."""
        # Log the error
        self.log_error(error, request)
        
        # Determine error details
        if isinstance(error, CredentialNotFoundError):
            title = "Credential Not Found"
            message = str(error)
            status_code = status.HTTP_404_NOT_FOUND
            advice = "The requested credentials were not found. Please check the environment name."
        elif isinstance(error, PasswordExpiredError):
            title = "Password Expired"
            message = str(error)
            status_code = status.HTTP_403_FORBIDDEN
            advice = "The password for this environment has expired. Please update it."
        elif isinstance(error, ValidationError):
            title = "Validation Error"
            message = str(error)
            status_code = status.HTTP_400_BAD_REQUEST
            advice = "Please check your input and try again."
        elif isinstance(error, BackendError):
            title = "Backend Error"
            message = str(error)
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            advice = "The credential storage backend is unavailable. Please check system configuration."
        elif isinstance(error, CredentialError):
            title = "Credential Error"
            message = str(error)
            status_code = status.HTTP_400_BAD_REQUEST
            advice = "There was an error with the credential operation."
        else:
            title = "Internal Server Error"
            message = "An unexpected error occurred."
            advice = "Please try again later or contact support."
        
        # Create error HTML
        error_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Error - {title}</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-gray-100">
            <div class="min-h-screen flex items-center justify-center px-4">
                <div class="max-w-md w-full bg-white rounded-lg shadow-lg p-6">
                    <div class="flex items-center justify-center w-12 h-12 mx-auto bg-red-100 rounded-full">
                        <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </div>
                    <h1 class="mt-4 text-xl font-semibold text-center text-gray-900">{title}</h1>
                    <p class="mt-2 text-center text-gray-600">{message}</p>
                    <p class="mt-4 text-sm text-center text-gray-500">{advice}</p>
                    <div class="mt-6">
                        <button onclick="window.history.back()" class="w-full px-4 py-2 text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500">
                            Go Back
                        </button>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return HTMLResponse(content=error_html, status_code=status_code)


# Global error handler instance
web_error_handler = WebErrorHandler()
```


## Utility Functions


```python # dbcreds/utils/shortcuts.py
# dbcreds/utils/shortcuts.py
"""
Convenience functions for common dbcreds operations.

This module provides simple shortcuts for the most common use cases,
making it easy to get started with dbcreds.
"""

from contextlib import contextmanager
from typing import Any, Dict, Optional

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


```


## Command-Line Interface


```python # dbcreds/cli.py
# dbcreds/cli.py
"""
Command-line interface for dbcreds.

This module provides a rich, user-friendly CLI for managing database
credentials using Typer and Rich.
"""

import os
import sys
from datetime import datetime
from typing import Optional

import typer
from loguru import logger
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

from dbcreds import __version__
from dbcreds.core.exceptions import CredentialError, CredentialNotFoundError
from dbcreds.core.manager import CredentialManager
from dbcreds.core.models import DatabaseType

# Configure logger for CLI
logger.remove()  # Remove default handler
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    level="INFO" if not os.getenv("DBCREDS_DEBUG") else "DEBUG",
)

app = typer.Typer(
    name="dbcreds",
    help="Professional database credentials management",
    add_completion=True,
    rich_markup_mode="rich",
)
console = Console()


def version_callback(value: bool):
    """Show version and exit."""
    if value:
        console.print(f"[bold blue]dbcreds[/bold blue] version [green]{__version__}[/green]")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    ),
):
    """
    dbcreds - Professional database credentials management.

    Securely store and manage database credentials for multiple environments.
    """
    pass


@app.command()
def init():
    """Initialize dbcreds configuration."""
    console.print("[bold blue]Initializing dbcreds...[/bold blue]")

    manager = CredentialManager()
    console.print(f"✅ Configuration directory: [green]{manager.config_dir}[/green]")
    console.print(f"✅ Available backends: [green]{len(manager.backends)}[/green]")

    for backend in manager.backends:
        console.print(f"  - {backend.__class__.__name__}")

    console.print("\n[bold green]dbcreds initialized successfully![/bold green]")


@app.command()
def add(
    name: str = typer.Argument(..., help="Environment name (e.g., dev, staging, prod)"),
    db_type: DatabaseType = typer.Option(
        DatabaseType.POSTGRESQL,
        "--type",
        "-t",
        help="Database type",
        case_sensitive=False,
    ),
    host: Optional[str] = typer.Option(None, "--host", "-h", help="Database host"),
    port: Optional[int] = typer.Option(None, "--port", "-p", help="Database port"),
    database: Optional[str] = typer.Option(None, "--database", "-d", help="Database name"),
    username: Optional[str] = typer.Option(None, "--username", "-u", help="Database username"),
    description: Optional[str] = typer.Option(None, "--description", help="Environment description"),
    production: bool = typer.Option(False, "--production", help="Mark as production environment"),
    expires_days: int = typer.Option(90, "--expires-days", help="Password expiry in days"),
):
    """Add a new database environment."""
    console.print(f"\n[bold blue]Adding environment: {name}[/bold blue]")

    manager = CredentialManager()

    # Check if environment already exists
    if name.lower() in [env.name for env in manager.list_environments()]:
        console.print(f"[red]Environment '{name}' already exists![/red]")
        if not Confirm.ask("Do you want to update the credentials?"):
            raise typer.Exit()
    else:
        # Add the environment
        try:
            manager.add_environment(name, db_type, description, production)
            console.print(f"✅ Created environment: [green]{name}[/green]")
        except CredentialError as e:
            console.print(f"[red]Error: {e}[/red]")
            raise typer.Exit(1)

    # Collect connection details
    if not host:
        host = Prompt.ask("Database host", default="localhost")
    if not port:
        default_ports = {
            DatabaseType.POSTGRESQL: 5432,
            DatabaseType.MYSQL: 3306,
            DatabaseType.ORACLE: 1521,
            DatabaseType.MSSQL: 1433,
        }
        port = IntPrompt.ask("Database port", default=default_ports.get(db_type, 5432))
    if not database:
        database = Prompt.ask("Database name")
    if not username:
        username = Prompt.ask("Username")

    # Get password securely
    password = Prompt.ask("Password", password=True)
    confirm_password = Prompt.ask("Confirm password", password=True)

    if password != confirm_password:
        console.print("[red]Passwords do not match![/red]")
        raise typer.Exit(1)

    # Store credentials
    try:
        manager.set_credentials(
            name,
            host,
            port,
            database,
            username,
            password,
            expires_days,
        )
        console.print(f"\n✅ Credentials stored for environment: [green]{name}[/green]")

        # Test connection
        if Confirm.ask("Test connection?", default=True):
            test(name)

    except Exception as e:
        console.print(f"[red]Error storing credentials: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def list():
    """List all configured environments."""
    manager = CredentialManager()
    environments = manager.list_environments()

    if not environments:
        console.print("[yellow]No environments configured yet.[/yellow]")
        console.print("Use [bold]dbcreds add[/bold] to add an environment.")
        return

    table = Table(title="Configured Environments", box=box.ROUNDED)
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Type", style="magenta")
    table.add_column("Description", style="green")
    table.add_column("Production", style="red")
    table.add_column("Created", style="blue")

    for env in environments:
        table.add_row(
            env.name,
            env.database_type.value,
            env.description or "-",
            "✓" if env.is_production else "",
            env.created_at.strftime("%Y-%m-%d"),
        )

    console.print(table)


@app.command()
def show(
    name: str = typer.Argument(..., help="Environment name"),
    show_password: bool = typer.Option(False, "--password", help="Show password"),
):
    """Show details for a specific environment."""
    manager = CredentialManager()

    try:
        creds = manager.get_credentials(name)
        env = next((e for e in manager.list_environments() if e.name == name.lower()), None)

        if not env:
            console.print(f"[red]Environment '{name}' not found![/red]")
            raise typer.Exit(1)

        # Create details panel
        details = f"""[bold cyan]Environment:[/bold cyan] {env.name}
[bold cyan]Type:[/bold cyan] {env.database_type.value}
[bold cyan]Description:[/bold cyan] {env.description or 'N/A'}
[bold cyan]Production:[/bold cyan] {'Yes' if env.is_production else 'No'}

[bold yellow]Connection Details:[/bold yellow]
[bold]Host:[/bold] {creds.host}
[bold]Port:[/bold] {creds.port}
[bold]Database:[/bold] {creds.database}
[bold]Username:[/bold] {creds.username}
[bold]Password:[/bold] {'*' * 8 if not show_password else creds.password.get_secret_value()}

[bold yellow]Password Status:[/bold yellow]
[bold]Last Updated:[/bold] {creds.password_updated_at.strftime('%Y-%m-%d %H:%M')}"""

        if creds.password_expires_at:
            days_left = creds.days_until_expiry()
            if days_left is not None:
                if days_left <= 0:
                    details += f"\n[bold red]Status: EXPIRED[/bold red]"
                elif days_left <= 14:
                    details += f"\n[bold yellow]Expires in: {days_left} days[/bold yellow]"
                else:
                    details += f"\n[bold green]Expires in: {days_left} days[/bold green]"

        panel = Panel(details, title=f"Environment: {name}", box=box.ROUNDED)
        console.print(panel)

    except CredentialNotFoundError:
        console.print(f"[red]No credentials found for environment '{name}'[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def test(
    name: str = typer.Argument(..., help="Environment name"),
):
    """Test database connection for an environment."""
    manager = CredentialManager()

    with console.status(f"Testing connection to [bold]{name}[/bold]..."):
        try:
            if manager.test_connection(name):
                console.print(f"✅ [green]Connection to '{name}' successful![/green]")
            else:
                console.print(f"❌ [red]Connection to '{name}' failed![/red]")
                raise typer.Exit(1)
        except Exception as e:
            console.print(f"❌ [red]Connection test failed: {e}[/red]")
            raise typer.Exit(1)


@app.command()
def remove(
    name: str = typer.Argument(..., help="Environment name"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """Remove an environment and its credentials."""
    if not force:
        if not Confirm.ask(f"Are you sure you want to remove environment '{name}'?"):
            console.print("[yellow]Cancelled[/yellow]")
            raise typer.Exit()

    manager = CredentialManager()

    try:
        manager.remove_environment(name)
        console.print(f"✅ [green]Environment '{name}' removed successfully![/green]")
    except CredentialNotFoundError:
        console.print(f"[red]Environment '{name}' not found![/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def update(
    name: str = typer.Argument(..., help="Environment name"),
    password: bool = typer.Option(False, "--password", help="Update password only"),
    expires_days: Optional[int] = typer.Option(None, "--expires-days", help="Update password expiry"),
):
    """Update credentials for an environment."""
    manager = CredentialManager()

    try:
        # Get existing credentials
        creds = manager.get_credentials(name, check_expiry=False)

        if password:
            # Update password only
            new_password = Prompt.ask("New password", password=True)
            confirm_password = Prompt.ask("Confirm new password", password=True)

            if new_password != confirm_password:
                console.print("[red]Passwords do not match![/red]")
                raise typer.Exit(1)

            manager.set_credentials(
                name,
                creds.host,
                creds.port,
                creds.database,
                creds.username,
                new_password,
                expires_days or 90,
            )
            console.print(f"✅ [green]Password updated for environment '{name}'[/green]")
        else:
            console.print("[yellow]Full credential update not implemented yet[/yellow]")

    except CredentialNotFoundError:
        console.print(f"[red]Environment '{name}' not found![/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def check():
    """Check for expiring or expired passwords."""
    manager = CredentialManager()
    environments = manager.list_environments()

    if not environments:
        console.print("[yellow]No environments configured.[/yellow]")
        return

    expired = []
    expiring_soon = []
    healthy = []

    with console.status("Checking password expiry..."):
        for env in environments:
            try:
                creds = manager.get_credentials(env.name, check_expiry=False)
                days = creds.days_until_expiry()

                if days is not None:
                    if days <= 0:
                        expired.append((env.name, abs(days)))
                    elif days <= 14:
                        expiring_soon.append((env.name, days))
                    else:
                        healthy.append((env.name, days))
                else:
                    healthy.append((env.name, None))
            except:
                # Skip environments without credentials
                pass

    # Display results
    if expired:
        console.print("\n[bold red]⚠️  Expired Passwords:[/bold red]")
        for name, days in expired:
            console.print(f"  - {name}: expired {days} days ago")

    if expiring_soon:
        console.print("\n[bold yellow]⚠️  Expiring Soon:[/bold yellow]")
        for name, days in expiring_soon:
            console.print(f"  - {name}: {days} days remaining")

    if healthy:
        console.print("\n[bold green]✅ Healthy:[/bold green]")
        for name, days in healthy[:5]:  # Show first 5
            if days:
                console.print(f"  - {name}: {days} days remaining")
            else:
                console.print(f"  - {name}: no expiry set")
        if len(healthy) > 5:
            console.print(f"  ... and {len(healthy) - 5} more")


@app.command()
def export(
    name: str = typer.Argument(..., help="Environment name"),
    format: str = typer.Option("uri", "--format", "-f", help="Export format (uri, env, json)"),
    include_password: bool = typer.Option(True, "--include-password", help="Include password"),
):
    """Export connection details for an environment."""
    manager = CredentialManager()

    try:
        creds = manager.get_credentials(name)

        if format == "uri":
            uri = creds.get_connection_string(include_password=include_password)
            console.print(uri)
        elif format == "env":
            env_name = name.upper()
            console.print(f"export DBCREDS_{env_name}_HOST={creds.host}")
            console.print(f"export DBCREDS_{env_name}_PORT={creds.port}")
            console.print(f"export DBCREDS_{env_name}_DATABASE={creds.database}")
            console.print(f"export DBCREDS_{env_name}_USERNAME={creds.username}")
            if include_password:
                console.print(f"export DBCREDS_{env_name}_PASSWORD={creds.password.get_secret_value()}")
        elif format == "json":
            import json

            data = {
                "host": creds.host,
                "port": creds.port,
                "database": creds.database,
                "username": creds.username,
            }
            if include_password:
                data["password"] = creds.password.get_secret_value()
            console.print(json.dumps(data, indent=2))
        else:
            console.print(f"[red]Unknown format: {format}[/red]")
            raise typer.Exit(1)

    except CredentialNotFoundError:
        console.print(f"[red]Environment '{name}' not found![/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()

```

```python # dbcreds/migrate.py
# dbcreds/migrate.py
"""
Migration script for importing existing PowerShell credentials into dbcreds.
"""

import os
import sys
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

from dbcreds.core.manager import CredentialManager
from dbcreds.core.models import DatabaseType

console = Console()


def detect_database_type(port: int, server: str = "") -> DatabaseType:
    """Detect database type from port or server name."""
    port_mapping = {
        5432: DatabaseType.POSTGRESQL,
        3306: DatabaseType.MYSQL,
        1433: DatabaseType.MSSQL,
        1521: DatabaseType.ORACLE,
    }
    
    # Check port first
    if port in port_mapping:
        return port_mapping[port]
    
    # Check server name for hints
    server_lower = server.lower()
    if "postgres" in server_lower or "pg" in server_lower or "rds" in server_lower:
        return DatabaseType.POSTGRESQL
    elif "mysql" in server_lower or "maria" in server_lower:
        return DatabaseType.MYSQL
    elif "mssql" in server_lower or "sqlserver" in server_lower:
        return DatabaseType.MSSQL
    elif "oracle" in server_lower:
        return DatabaseType.ORACLE
    
    # Default to PostgreSQL
    return DatabaseType.POSTGRESQL


def main(
    env_name: str = typer.Option("default", "--name", "-n", help="Environment name for dbcreds"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite if exists"),
):
    """Import credentials from PowerShell environment variables."""
    console.print("[bold blue]Importing credentials from PowerShell environment...[/bold blue]")
    
    # Check for required environment variables
    required_vars = ["DB_SERVER", "DB_PORT", "DB_NAME", "DB_USER"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        console.print(f"[red]Missing environment variables: {', '.join(missing_vars)}[/red]")
        console.print("[yellow]Please run your PowerShell profile first to set up the environment.[/yellow]")
        console.print("\nTry running these commands first:")
        console.print("  Connect-ODS")
        console.print("  # or")
        console.print("  update-db")
        sys.exit(1)
    
    # Get values from environment
    server = os.environ.get("DB_SERVER")
    port = int(os.environ.get("DB_PORT", 5432))
    database = os.environ.get("DB_NAME")
    username = os.environ.get("DB_USER")
    password = os.environ.get("DB_PWD")
    
    # Try to get password from Windows Credential Manager if not in env
    if not password:
        try:
            from dbcreds.backends.legacy_windows import LegacyWindowsBackend
            backend = LegacyWindowsBackend()
            legacy_target = f"DBCredentials:{database}"
            password = backend._get_password_from_legacy_target(legacy_target)
            if password:
                console.print("[green]Retrieved password from Windows Credential Manager[/green]")
        except Exception as e:
            console.print(f"[yellow]Could not retrieve password from Credential Manager: {e}[/yellow]")
    
    if not password:
        console.print("[red]No password found in environment or Credential Manager![/red]")
        console.print("\nMake sure you have run one of these commands:")
        console.print("  update-db")
        console.print("  Set-DatabaseEnvironment")
        sys.exit(1)
    
    # Detect database type
    db_type = detect_database_type(port, server)
    
    # Show what will be imported
    panel = Panel(
        f"""[cyan]Server:[/cyan] {server}
[cyan]Port:[/cyan] {port}
[cyan]Database:[/cyan] {database}
[cyan]Username:[/cyan] {username}
[cyan]Password:[/cyan] ********
[cyan]Type:[/cyan] {db_type.value}
[cyan]Environment:[/cyan] {env_name}""",
        title="Credentials to Import",
        border_style="green",
    )
    console.print(panel)
    
    # Confirm import
    if not Confirm.ask("Import these credentials?"):
        console.print("[yellow]Import cancelled.[/yellow]")
        return
    
    # Import into dbcreds
    manager = CredentialManager()
    
    try:
        # Check if environment exists
        existing_envs = [env.name for env in manager.list_environments()]
        if env_name in existing_envs:
            if not force:
                console.print(f"[yellow]Environment '{env_name}' already exists![/yellow]")
                if not Confirm.ask("Overwrite existing credentials?"):
                    return
        else:
            # Add the environment
            manager.add_environment(
                env_name, 
                db_type,
                description=f"Imported from PowerShell ({database})",
                is_production=False
            )
        
        # Set credentials
        expiry_days = int(os.environ.get("DB_PWD_EXPIRY", 90))
        manager.set_credentials(
            env_name,
            server,
            port,
            database,
            username,
            password,
            expiry_days,
        )
        
        console.print(f"\n[green]✓ Successfully imported credentials to environment '{env_name}'[/green]")
        
        # Test connection
        if Confirm.ask("\nTest the connection?"):
            console.print("\n[cyan]Testing connection...[/cyan]")
            if manager.test_connection(env_name):
                console.print("[green]✓ Connection test successful![/green]")
            else:
                console.print("[red]✗ Connection test failed![/red]")
                console.print("[yellow]Check that psycopg2 is installed: uv pip install psycopg2-binary[/yellow]")
                
    except Exception as e:
        console.print(f"[red]Error importing credentials: {e}[/red]")
        if "psycopg2" in str(e):
            console.print("\n[yellow]Install psycopg2 with: uv pip install psycopg2-binary[/yellow]")
        sys.exit(1)


if __name__ == "__main__":
    typer.run(main)
```