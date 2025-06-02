# dbcreds Reference

Auto-generated on 2025-06-02 18:12:04


This file contains the latest source code for the dbcreds library.



## Directory Structure


Project organization showing the key files and their relationships:



```
dbcreds/
├── __init__.py
├── __init__.py.backup.20250602_164416
├── cli.py
├── export_fast.py
├── fast.py
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
│   ├── manager.py.backup.20250602_164416
│   ├── models.py
│   └── security.py
├── utils/
│   ├── __init__.py
│   ├── shortcuts.py
│   └── shortcuts.py.backup.20250602_164416
└── web/
    ├── __init__.py
    ├── __main__.py
    ├── auth.py
    ├── errors.py
    ├── main.py
    ├── static/
    │   ├── favicon-16x16.png
    │   ├── favicon-32x32.png
    │   ├── favicon.ico
    │   ├── logo.svg
    │   └── css/
    │       └── custom.css
    └── templates/
        ├── base.html
        ├── index.html
        ├── settings.html
        └── partials/
            └── environment_list.html
```

``` # LICENSE
MIT License

Copyright (c) 2025 Thandolwethu Dlamini

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```

<p align="center">
  <img src="docs/assets/images/logo.png" alt="dbcreds logo" width="128">
</p>

<h1 align="center">dbcreds</h1>

<p align="center">
  Professional database credentials management with security and team collaboration in mind.
</p>

## Features

--8<-- "docs/includes/features-list.md"

## Installation

--8<-- "docs/includes/installation-full.md"

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

--8<-- "docs/includes/python-examples.md"

## CLI Usage

--8<-- "docs/includes/cli-examples.md"

## Web Interface

Start the web interface for team credential management:

```bash
dbcreds-server
# Visit http://localhost:8000
```

## Configuration

dbcreds stores configuration in `~/.dbcreds/config.json` and credentials in your system's secure storage.

## Development

--8<-- "docs/includes/development.md"

## Security

- Credentials are never stored in plain text
- Each environment has isolated credentials
- Password rotation reminders
- Audit logging for credential access
- Team-based access control in web UI

## License

MIT License - see LICENSE file for details.

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
    "httpx>=0.28.1",
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
dbcreds-export-fast = "dbcreds.export_fast:main"

[project.urls]
Homepage = "https://github.com/yourcompany/dbcreds"
Documentation = "https://yourcompany.github.io/dbcreds"
Repository = "https://github.com/Sunnova-ShakesDlamini/dbcreds"
Issues = "https://github.com/Sunnova-ShakesDlamini/dbcreds/issues"

[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
packages = ["dbcreds", "dbcreds.backends", "dbcreds.core", "dbcreds.web", "dbcreds.utils"]

[tool.setuptools.package-data]
"dbcreds.web" = ["templates/*.html", "templates/**/*.html"]

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
asyncio_default_fixture_loop_scope = "function"
filterwarnings = [
    "ignore::DeprecationWarning:fastapi",
    "ignore::DeprecationWarning:pytest_asyncio.plugin",
]

# uv configuration
[tool.uv]
managed = true
dev-dependencies = [
    "ipython>=8.12.0",
    "ipdb>=0.13.13",
]

```


## Core


```python # dbcreds\__init__.py
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

```

```python # dbcreds\backends\__init__.py
# dbcreds/backends/__init__.py
"""Credential storage backends."""

# Remove all imports - just define __all__
__all__ = ["CredentialBackend", "ConfigFileBackend", "EnvironmentBackend", "KeyringBackend"]

# No actual imports here - let modules import directly from submodules
```

```python # dbcreds\core\__init__.py
# dbcreds/core/__init__.py
"""Core functionality for dbcreds."""

from dbcreds.core.manager import CredentialManager
from dbcreds.core.models import DatabaseCredentials, DatabaseType, Environment

__all__ = ["CredentialManager", "DatabaseCredentials", "DatabaseType", "Environment"]


```

```python # dbcreds\core\exceptions.py
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

```python # dbcreds\core\manager.py
# dbcreds/core/manager.py
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

```

```python # dbcreds\core\models.py
# dbcreds/core/models.py
"""
Pydantic models for database credentials.

This module defines the data models used throughout dbcreds for type safety
and validation.
"""

from datetime import datetime, timezone
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
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate environment name."""
        return v.lower()

    @field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def ensure_timezone_aware(cls, v):
        """Ensure datetime fields are timezone-aware."""
        if v is None:
            return v
        if isinstance(v, str):
            # If it's a string, let Pydantic parse it
            return v
        if isinstance(v, datetime) and v.tzinfo is None:
            # If it's a naive datetime, assume UTC
            return v.replace(tzinfo=timezone.utc)
        return v


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
    password_updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
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

    @field_validator("password_updated_at", "password_expires_at", mode="before")
    @classmethod
    def ensure_timezone_aware(cls, v):
        """Ensure datetime fields are timezone-aware."""
        if v is None:
            return v
        if isinstance(v, str):
            # If it's a string, let Pydantic parse it
            return v
        if isinstance(v, datetime) and v.tzinfo is None:
            # If it's a naive datetime, assume UTC
            return v.replace(tzinfo=timezone.utc)
        return v

    def get_connection_string(
        self, include_password: bool = True, driver: Optional[str] = None
    ) -> str:
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
        password_part = (
            f":{self.password.get_secret_value()}" if include_password else ""
        )
        return f"postgresql://{self.username}{password_part}@{self.host}:{self.port}/{self.database}"

    def is_password_expired(self) -> bool:
        """Check if the password has expired."""
        if self.password_expires_at is None:
            return False

        # Ensure both datetimes are timezone-aware for comparison
        expires_at = self.password_expires_at
        if expires_at.tzinfo is None:
            # If naive, assume it was UTC
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        return datetime.now(timezone.utc) > expires_at

    def days_until_expiry(self) -> Optional[int]:
        """Get the number of days until password expiry."""
        if self.password_expires_at is None:
            return None

        # Ensure both datetimes are timezone-aware for comparison
        expires_at = self.password_expires_at
        if expires_at.tzinfo is None:
            # If naive, assume it was UTC
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        delta = expires_at - datetime.now(timezone.utc)
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
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_accessed: Optional[datetime] = None
    access_count: int = 0
    last_tested: Optional[datetime] = None
    last_test_success: Optional[bool] = None

    @field_validator("created_at", "last_accessed", "last_tested", mode="before")
    @classmethod
    def ensure_timezone_aware(cls, v):
        """Ensure datetime fields are timezone-aware."""
        if v is None:
            return v
        if isinstance(v, str):
            # If it's a string, let Pydantic parse it
            return v
        if isinstance(v, datetime) and v.tzinfo is None:
            # If it's a naive datetime, assume UTC
            return v.replace(tzinfo=timezone.utc)
        return v

```

```python # dbcreds\core\security.py
# dbcreds/core/security.py
"""Security utilities for dbcreds."""

import re
from typing import Any, Dict

from dbcreds.core.exceptions import ValidationError


def sanitize_environment_name(name: str) -> str:
    """Sanitize environment name to prevent injection attacks."""
    if not re.match(r"^[a-zA-Z0-9_-]+$", name):
        raise ValidationError(
            "Environment name can only contain letters, numbers, hyphens, and underscores"
        )
    return name.lower()


def sanitize_connection_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize connection parameters."""
    # Remove any potentially dangerous keys
    dangerous_keys = ["password", "passwd", "pwd"]
    sanitized = {k: v for k, v in params.items() if k.lower() not in dangerous_keys}
    
    # Validate host
    if "host" in sanitized:
        if not re.match(r"^[a-zA-Z0-9.-]+$", sanitized["host"]):
            raise ValidationError("Invalid host format")
    
    # Validate port
    if "port" in sanitized:
        try:
            port = int(sanitized["port"])
            if not 1 <= port <= 65535:
                raise ValidationError("Port must be between 1 and 65535")
        except (ValueError, TypeError):
            raise ValidationError("Invalid port number")
    
    return sanitized


def mask_password(connection_string: str) -> str:
    """Mask password in connection strings for logging."""
    # Pattern to match passwords in various connection string formats
    patterns = [
        r"(password=)([^;]+)",
        r"(pwd=)([^;]+)",
        r"(:\/\/[^:]+:)([^@]+)(@)",
    ]
    
    masked = connection_string
    for pattern in patterns:
        masked = re.sub(pattern, r"\1****\3", masked, flags=re.IGNORECASE)
    
    return masked

```

```python # dbcreds\utils\__init__.py
# dbcreds/utils/__init__.py
"""Utility functions and shortcuts for dbcreds."""

from dbcreds.utils.shortcuts import (
    get_async_engine,
    get_connection,
    get_connection_string,
    get_credentials,
    get_engine,
)

__all__ = [
    "get_connection",
    "get_engine",
    "get_async_engine",
    "get_credentials",
    "get_connection_string",
]


```

```python # dbcreds\web\__init__.py
# dbcreds/web/__init__.py
"""Web interface for dbcreds using FastAPI and HTMX."""


```


## Backends


```python # dbcreds\backends\base.py
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

```python # dbcreds\backends\config.py
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

```python # dbcreds\backends\environment.py
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

```python # dbcreds\backends\keyring.py
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

```python # dbcreds\backends\legacy_windows.py
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

```python # dbcreds\backends\windows.py
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


## Web Interface


```python # dbcreds\web\auth.py
# dbcreds/web/auth.py
"""Authentication for the web interface."""

import secrets
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# Configuration
SECRET_KEY = secrets.token_urlsafe(32)  # In production, load from environment
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()

# Default admin credentials - CHANGE IN PRODUCTION
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD_HASH = pwd_context.hash("changeme")


class Token(BaseModel):
    access_token: str
    token_type: str


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str) -> bool:
    """Authenticate a user."""
    if username == DEFAULT_USERNAME:
        return verify_password(password, DEFAULT_PASSWORD_HASH)
    return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    """Get the current authenticated user."""
    if not authenticate_user(credentials.username, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

```

```python # dbcreds\web\errors.py
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

```python # dbcreds\web\main.py
# dbcreds/web/main.py
"""
FastAPI web application for dbcreds.

Provides a web interface for managing database credentials with
team collaboration features.
"""

import os
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install as install_rich_traceback

from dbcreds import __version__
from dbcreds.core.exceptions import CredentialError
from dbcreds.core.manager import CredentialManager
from dbcreds.core.models import DatabaseType
from dbcreds.web.errors import web_error_handler

# Install rich traceback handler
install_rich_traceback(show_locals=True)

# Create console for startup messages
console = Console()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    console.print(
        Panel.fit(
            f"[bold green]dbcreds Web Server v{__version__}[/bold green]\n"
            f"[dim]Ready to manage your database credentials[/dim]",
            title="Starting Up",
            border_style="green",
        )
    )
    yield
    # Shutdown (if needed)


# Create FastAPI app
app = FastAPI(
    title="dbcreds Web",
    description="Database Credentials Management",
    version=__version__,
    lifespan=lifespan,
)

# Add middleware
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
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )
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
        logger.error(f"Error loading settings page: {e}")
        return HTMLResponse(
            content=f'<div class="text-red-600 p-4">Error loading settings: {str(e)}</div>',
            status_code=500,
        )


# Updated create_environment function for dbcreds/web/main.py


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
            is_production=bool(form_data.get("is_production", False)),
        )

        # Get password update date if provided
        password_updated_at = None
        password_updated_at_str = form_data.get("password_updated_at", "").strip()
        if password_updated_at_str:
            try:
                # Parse as naive datetime then make timezone aware
                naive_dt = datetime.strptime(password_updated_at_str, "%Y-%m-%d")
                password_updated_at = naive_dt.replace(tzinfo=timezone.utc)
            except ValueError:
                # If parsing fails, use current date
                password_updated_at = None

        # Set credentials
        expires_days = int(form_data.get("expires_days", 90))
        manager.set_credentials(
            env_name,
            host=form_data.get("host"),
            port=int(form_data.get("port", 5432)),
            database=form_data.get("database"),
            username=form_data.get("username"),
            password=form_data.get("password"),
            password_expires_days=expires_days,
        )

        # If a custom password update date was provided, update it
        if password_updated_at:
            # Update the password_updated_at field in the backend
            for backend in manager.backends:
                if backend.is_available():
                    try:
                        # Get the credential we just stored
                        result = backend.get_credential(f"dbcreds:{env_name}")
                        if result:
                            username, password, metadata = result
                            # Update the password_updated_at field
                            metadata["password_updated_at"] = (
                                password_updated_at.isoformat()
                            )
                            # Recalculate expiry based on the custom date
                            if expires_days > 0:
                                expires_at = password_updated_at + timedelta(
                                    days=expires_days
                                )
                                metadata["password_expires_at"] = expires_at.isoformat()
                            # Save back to the backend
                            backend.set_credential(
                                f"dbcreds:{env_name}", username, password, metadata
                            )
                            break
                    except Exception as backend_error:
                        logger.error(
                            f"Error updating password date in backend: {backend_error}"
                        )

        # Get updated environments list
        environments = manager.list_environments()

        # Return response with environment list, close modal, and show success
        return HTMLResponse(
            content=f"""
            <div id="environment-list" hx-swap-oob="true">
                {
                templates.get_template("partials/environment_list.html").render(
                    request=request, environments=environments
                )
            }
            </div>
            <div id="modal" hx-swap-oob="true"></div>
            <div id="notification-container" hx-swap-oob="afterbegin">
                <div class="fixed top-4 right-4 z-50 animate-fade-in-down">
                    <div class="bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded-lg shadow-lg flex items-center space-x-3">
                        <svg class="h-5 w-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                        </svg>
                        <span class="font-medium">Environment '{
                env_name
            }' created successfully!</span>
                    </div>
                </div>
                <script>
                    // Remove notification after 3 seconds
                    setTimeout(() => {{
                        const notification = document.querySelector('#notification-container > div');
                        if (notification) {{
                            notification.classList.add('animate-fade-out-up');
                            setTimeout(() => notification.remove(), 300);
                        }}
                    }}, 3000);
                    
                    // Reload expiry info for all environments
                    setTimeout(loadAllExpiryInfo, 100);
                </script>
            </div>
            """
        )
    except Exception as e:
        return HTMLResponse(
            content=f"""
            <div id="notification-container" hx-swap-oob="afterbegin">
                <div class="fixed top-4 right-4 z-50 animate-fade-in-down">
                    <div class="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg shadow-lg flex items-center space-x-3">
                        <svg class="h-5 w-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                        <span class="font-medium">Error: {str(e)}</span>
                    </div>
                </div>
                <script>
                    // Remove notification after 5 seconds
                    setTimeout(() => {{
                        const notification = document.querySelector('#notification-container > div');
                        if (notification) {{
                            notification.classList.add('animate-fade-out-up');
                            setTimeout(() => notification.remove(), 300);
                        }}
                    }}, 5000);
                </script>
            </div>
            """,
            status_code=400,
        )


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
            status_code=500,
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
                "available": backend.is_available(),
            }

            # Add descriptions for known backends
            if "Keyring" in backend_name:
                backend_info["description"] = (
                    "System keyring (Keychain on macOS, Credential Manager on Windows)"
                )
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
    except Exception:
        # Errors will be caught by exception handlers
        raise


@app.get("/environments/{env_name}/edit", response_class=HTMLResponse)
async def edit_environment_form(request: Request, env_name: str):
    """Get edit form for an environment."""
    try:
        manager = CredentialManager()
        creds = manager.get_credentials(env_name, check_expiry=False)
        env = next((e for e in manager.list_environments() if e.name == env_name), None)

        if not env:
            raise HTTPException(status_code=404, detail="Environment not found")

        # Helper function to ensure timezone-aware datetime
        def ensure_timezone_aware(dt):
            if dt and dt.tzinfo is None:
                return dt.replace(tzinfo=timezone.utc)
            return dt

        # Ensure datetimes are timezone-aware
        password_updated_at = ensure_timezone_aware(creds.password_updated_at)
        password_expires_at = ensure_timezone_aware(creds.password_expires_at)

        # Calculate days until expiry
        days_left = None
        expiry_period = 90  # Default

        if password_expires_at and password_updated_at:
            # Calculate the total expiry period (not the days left)
            expiry_period = (password_expires_at - password_updated_at).days
            # Calculate days left
            delta = password_expires_at - datetime.now(timezone.utc)
            days_left = delta.days if delta.days > 0 else 0
        elif password_updated_at:
            # If we have updated_at but no expires_at, still show it will expire
            # Calculate what the expiry date would be with default 90 days
            theoretical_expires_at = password_updated_at + timedelta(days=expiry_period)
            delta = theoretical_expires_at - datetime.now(timezone.utc)
            days_left = delta.days if delta.days > 0 else 0

        # Determine password status HTML
        if password_expires_at is None and password_updated_at:
            # Has update date but no expiry set - show calculated expiry
            password_status_html = f"""
            <span class="text-yellow-600">No expiry stored (would expire in {days_left} days)</span>
            """
        elif creds.is_password_expired():
            password_status_html = """
            <span class="text-red-600">Expired</span>
            """
        elif days_left is not None:
            if days_left <= 7:
                password_status_html = f"""
                <span class="text-red-600">{days_left} days remaining</span>
                """
            elif days_left <= 30:
                password_status_html = f"""
                <span class="text-yellow-600">{days_left} days remaining</span>
                """
            else:
                password_status_html = f"""
                <span class="text-green-600">{days_left} days remaining</span>
                """
        else:
            password_status_html = """
            <span class="text-gray-600">No expiry set</span>
            """

        # Add details about dates
        date_details_html = '<div class="text-xs text-gray-500 mt-1">'
        if password_updated_at:
            date_details_html += (
                f"Last updated: {password_updated_at.strftime('%Y-%m-%d')}"
            )
        if password_expires_at:
            date_details_html += (
                f"<br>Expires on: {password_expires_at.strftime('%Y-%m-%d')}"
            )
        elif password_updated_at and expiry_period > 0:
            theoretical_expires = password_updated_at + timedelta(days=expiry_period)
            date_details_html += f"<br>Would expire on: {theoretical_expires.strftime('%Y-%m-%d')} (not stored)"
        date_details_html += "</div>"

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
                            <form hx-put="/environments/{env_name}" 
                                hx-target="#environment-list" 
                                hx-swap="innerHTML"
                                hx-indicator="#form-indicator">
                                <!-- Add hidden loading indicator -->
                                <div id="form-indicator" class="htmx-indicator fixed inset-0 bg-gray-500 bg-opacity-50 flex items-center justify-center rounded-lg" style="display:none;">
                                    <div class="bg-white p-4 rounded-lg shadow-lg flex items-center space-x-3">
                                        <svg class="animate-spin h-5 w-5 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                        </svg>
                                        <span class="text-gray-700">Updating environment...</span>
                                    </div>
                                </div>
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
                                            {password_status_html}
                                            {date_details_html}
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
                                               value="{password_updated_at.strftime("%Y-%m-%d") if password_updated_at else ""}"
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
                                            {'''<br><span class="text-yellow-600">Note: Updating this will set the expiry date.</span>''' if password_expires_at is None else ""}
                                        </p>
                                    </div>
                                </div>
                                
                                <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                                    <button type="submit"
                                            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:col-start-2 sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
                                            onclick="this.disabled=true; this.form.submit();">
                                        Update
                                    </button>
                                    <button type="button" 
                                            onclick="document.getElementById('modal').innerHTML=''"
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
            status_code=500,
        )


# Updated update_environment function for dbcreds/web/main.py


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
            # Parse the date from the form
            try:
                # Parse as naive datetime then make timezone aware
                naive_dt = datetime.strptime(new_update_date_str, "%Y-%m-%d")
                password_updated_at = naive_dt.replace(tzinfo=timezone.utc)
            except ValueError:
                return HTMLResponse(
                    content='<div class="text-red-600 p-4">Error: Invalid date format</div>',
                    status_code=400,
                )

        # Update password or other fields if needed
        new_password = form_data.get("password", "").strip()

        # If there's no password_expires_at but we have updated_at and expires_days,
        # we should update to add the expiry
        needs_expiry_fix = (
            creds.password_expires_at is None
            and (creds.password_updated_at or password_updated_at)
            and expires_days > 0
        )

        # Always consider an update needed if expiry days are set or needs fixing
        update_needed = (
            new_password or password_updated_at or expires_days > 0 or needs_expiry_fix
        )

        if update_needed:
            # We need to update the credentials
            if not new_password:
                # If only changing the update date or expiry, reuse existing password
                new_password = creds.password.get_secret_value()

            # Use the provided update date or existing one
            if not password_updated_at:
                password_updated_at = creds.password_updated_at
                # Ensure it's timezone aware
                if password_updated_at and password_updated_at.tzinfo is None:
                    password_updated_at = password_updated_at.replace(
                        tzinfo=timezone.utc
                    )

            # Always set credentials with expiry days to ensure expiry is calculated
            manager.set_credentials(
                env_name,
                host=creds.host,
                port=creds.port,
                database=creds.database,
                username=creds.username,
                password=new_password,
                password_expires_days=expires_days if expires_days > 0 else None,
            )

            # If we need to modify the update date, update it in the backend
            if password_updated_at and password_updated_at != creds.password_updated_at:
                # We need to update the password_updated_at field directly
                for backend in manager.backends:
                    if backend.is_available():
                        try:
                            # Get the raw credentials from the backend
                            result = backend.get_credential(f"dbcreds:{env_name}")
                            if result:
                                username, password, metadata = result
                                # Update the password_updated_at field in metadata
                                metadata["password_updated_at"] = (
                                    password_updated_at.isoformat()
                                )
                                # Always calculate the new expiry date if expires_days is set
                                if expires_days > 0:
                                    expires_at = password_updated_at + timedelta(
                                        days=expires_days
                                    )
                                    metadata["password_expires_at"] = (
                                        expires_at.isoformat()
                                    )
                                # Save back to the backend
                                backend.set_credential(
                                    f"dbcreds:{env_name}", username, password, metadata
                                )
                                break
                        except Exception as backend_error:
                            logger.error(
                                f"Error updating credentials in backend {backend.__class__.__name__}: {backend_error}"
                            )
                            continue

            # Log what we did
            logger.info(
                f"Updated environment {env_name}: password_changed={bool(form_data.get('password'))}, "
                f"date_updated={bool(password_updated_at != creds.password_updated_at)}, "
                f"expiry_fixed={needs_expiry_fix}"
            )

        # Get updated environments list
        environments = manager.list_environments()

        # Return response with environment list and trigger events
        return HTMLResponse(
            content=f"""
            <div id="environment-list" hx-swap-oob="true">
                {
                templates.get_template("partials/environment_list.html").render(
                    request=request, environments=environments
                )
            }
            </div>
            <div id="modal" hx-swap-oob="true"></div>
            <div id="notification-container" hx-swap-oob="afterbegin">
                <div class="fixed top-4 right-4 z-50 animate-fade-in-down">
                    <div class="bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded-lg shadow-lg flex items-center space-x-3">
                        <svg class="h-5 w-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                        </svg>
                        <span class="font-medium">Environment '{
                env_name
            }' updated successfully!</span>
                    </div>
                </div>
                <script>
                    // Remove notification after 3 seconds
                    setTimeout(() => {{
                        const notification = document.querySelector('#notification-container > div');
                        if (notification) {{
                            notification.classList.add('animate-fade-out-up');
                            setTimeout(() => notification.remove(), 300);
                        }}
                    }}, 3000);
                    
                    // Reload expiry info for the updated environment
                    setTimeout(() => loadExpiryInfo('{env_name}'), 100);
                </script>
            </div>
            """
        )
    except Exception as e:
        logger.error(f"Error updating environment {env_name}: {e}")
        return HTMLResponse(
            content=f"""
            <div class="text-red-600 p-4">Error: {str(e)}</div>
            <div id="notification-container" hx-swap-oob="afterbegin">
                <div class="fixed top-4 right-4 z-50 animate-fade-in-down">
                    <div class="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg shadow-lg flex items-center space-x-3">
                        <svg class="h-5 w-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                        <span class="font-medium">Error updating environment: {str(e)}</span>
                    </div>
                </div>
                <script>
                    // Remove notification after 5 seconds
                    setTimeout(() => {{
                        const notification = document.querySelector('#notification-container > div');
                        if (notification) {{
                            notification.classList.add('animate-fade-out-up');
                            setTimeout(() => notification.remove(), 300);
                        }}
                    }}, 5000);
                </script>
            </div>
            """,
            status_code=400,
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
            status_code=500,
        )


@app.get("/environments/new", response_class=HTMLResponse)
async def new_environment_form(request: Request):
    """New environment form (HTMX modal)."""
    # Default ports for each database type
    default_ports = {
        DatabaseType.POSTGRESQL: 5432,
        DatabaseType.MYSQL: 3306,
        DatabaseType.MSSQL: 1433,
        DatabaseType.ORACLE: 1521,
    }

    # Get today's date for the default
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    return HTMLResponse(
        content=f"""
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
                        <form hx-post="/environments" 
                              hx-target="#environment-list" 
                              hx-swap="innerHTML"
                              hx-indicator="#form-indicator">
                            <!-- Loading indicator -->
                            <div id="form-indicator" class="htmx-indicator fixed inset-0 bg-gray-500 bg-opacity-50 flex items-center justify-center rounded-lg" style="display:none;">
                                <div class="bg-white p-4 rounded-lg shadow-lg flex items-center space-x-3">
                                    <svg class="animate-spin h-5 w-5 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    <span class="text-gray-700">Creating environment...</span>
                                </div>
                            </div>
                            
                            <div class="space-y-4 max-h-[60vh] overflow-y-auto pr-2">
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
                                        {"".join(f'<option value="{dt.value}" data-port="{default_ports.get(dt, 5432)}">{dt.value.title()}</option>' for dt in DatabaseType)}
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
                                
                                <!-- Separator line for password management section -->
                                <div class="border-t border-gray-200 pt-4">
                                    <h4 class="text-sm font-medium text-gray-700 mb-3">Password Management</h4>
                                    
                                    <div>
                                        <label for="password_updated_at" class="block text-sm font-medium text-gray-700">
                                            Password Last Updated Date
                                        </label>
                                        <input type="date" name="password_updated_at" id="password_updated_at"
                                               value="{today}"
                                               max="{today}"
                                               class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                               onchange="updateExpiryPreview()">
                                        <p class="mt-1 text-xs text-gray-500">
                                            When was this password last set or changed? Defaults to today.
                                        </p>
                                    </div>
                                    
                                    <div class="mt-4">
                                        <label for="expires_days" class="block text-sm font-medium text-gray-700">
                                            Password Expiry Period (days)
                                        </label>
                                        <input type="number" name="expires_days" id="expires_days" value="90" min="0"
                                               class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                               oninput="updateExpiryPreview()">
                                        <p class="mt-1 text-xs text-gray-500">
                                            How many days until the password expires from the update date. Set to 0 to disable expiry.
                                        </p>
                                        <p id="expiry-preview" class="mt-1 text-xs"></p>
                                    </div>
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
        
        function updateExpiryPreview() {{
            const updateDateInput = document.getElementById('password_updated_at');
            const expireDaysInput = document.getElementById('expires_days');
            
            const updateDate = updateDateInput.value;
            const expireDays = parseInt(expireDaysInput.value) || 0;
            
            if (updateDate && expireDays > 0) {{
                const date = new Date(updateDate + 'T00:00:00Z');
                date.setDate(date.getDate() + expireDays);
                
                const expiryDate = date.toLocaleDateString('en-US', {{
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                }});
                
                // Check if already expired
                const today = new Date();
                today.setHours(0, 0, 0, 0);
                
                const daysUntilExpiry = Math.floor((date - today) / (1000 * 60 * 60 * 24));
                
                let message = `Password will expire on ${{expiryDate}}`;
                let className = 'text-gray-600';
                
                if (daysUntilExpiry < 0) {{
                    message = `Password would have expired on ${{expiryDate}} (${{Math.abs(daysUntilExpiry)}} days ago)`;
                    className = 'text-red-600';
                }} else if (daysUntilExpiry === 0) {{
                    message = `Password expires today!`;
                    className = 'text-red-600 font-medium';
                }} else if (daysUntilExpiry <= 7) {{
                    message = `Password will expire on ${{expiryDate}} (in ${{daysUntilExpiry}} days)`;
                    className = 'text-red-600';
                }} else if (daysUntilExpiry <= 30) {{
                    message = `Password will expire on ${{expiryDate}} (in ${{daysUntilExpiry}} days)`;
                    className = 'text-yellow-600';
                }} else {{
                    message = `Password will expire on ${{expiryDate}} (in ${{daysUntilExpiry}} days)`;
                    className = 'text-green-600';
                }}
                
                // Update preview
                const preview = document.getElementById('expiry-preview');
                preview.className = `mt-1 text-xs ${{className}}`;
                preview.textContent = message;
            }} else if (expireDays === 0) {{
                const preview = document.getElementById('expiry-preview');
                preview.className = 'mt-1 text-xs text-blue-600';
                preview.textContent = 'Password expiry tracking disabled';
            }} else {{
                // Clear preview
                const preview = document.getElementById('expiry-preview');
                preview.textContent = '';
            }}
        }}
        
        // Initial calculation
        updateExpiryPreview();
    </script>
    """
    )


@app.get("/api/environments/{env_name}/expiry")
async def get_environment_expiry(env_name: str):
    """Get password expiry information for an environment."""
    try:
        manager = CredentialManager()
        creds = manager.get_credentials(env_name, check_expiry=False)

        # Helper function to ensure datetime is timezone-aware
        def ensure_timezone_aware(dt):
            if dt and dt.tzinfo is None:
                # If naive, assume it was UTC
                return dt.replace(tzinfo=timezone.utc)
            return dt

        # Calculate days until expiry
        days_left = None
        expiry_days = 90  # Default value

        # Ensure all datetimes are timezone-aware
        password_updated_at = ensure_timezone_aware(creds.password_updated_at)
        password_expires_at = ensure_timezone_aware(creds.password_expires_at)

        if password_expires_at and password_updated_at:
            # We have both dates - calculate actual values
            expiry_days = (password_expires_at - password_updated_at).days
            # Calculate days left until expiry
            now_utc = datetime.now(timezone.utc)
            delta = password_expires_at - now_utc
            days_left = max(0, delta.days)  # Use max to avoid negative days
        elif password_updated_at:
            # We have updated_at but no expires_at
            # This means expiry is not being tracked, but we can calculate theoretical expiry
            # Don't set days_left here - let the frontend calculate it if needed
            pass

        # Check if expired
        is_expired = False
        if password_expires_at:
            is_expired = datetime.now(timezone.utc) > password_expires_at

        return {
            "days_left": days_left,
            "is_expired": is_expired,
            "expires_at": password_expires_at.isoformat()
            if password_expires_at
            else None,
            "updated_at": password_updated_at.isoformat()
            if password_updated_at
            else None,
            "has_expiry": password_expires_at
            is not None,  # Only true if actually tracking expiry
            "expires_days": expiry_days,  # Always return this so frontend can calculate
        }
    except Exception as e:
        logger.error(f"Error getting expiry for {env_name}: {e}")
        import traceback

        logger.error(traceback.format_exc())
        return {
            "error": str(e),
            "days_left": None,
            "is_expired": False,
            "updated_at": None,
            "has_expiry": False,
            "expires_days": 90,  # Default
        }


def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """Run the web server."""
    console.print("\n[bold blue]Starting dbcreds web server[/bold blue]")
    console.print(f"[green]➜[/green] Local:   http://localhost:{port}")
    console.print(f"[green]➜[/green] Network: http://{host}:{port}\n")

    # Configure uvicorn with custom logging
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["default"]["fmt"] = "%(levelprefix)s %(message)s"
    log_config["formatters"]["access"]["fmt"] = (
        '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
    )

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


## Utils


```python # dbcreds\utils\shortcuts.py
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

```


## CLI


```python # dbcreds\cli.py
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

```python # dbcreds\web\__main__.py
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


## Migrations


```python # dbcreds\migrate.py
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


## Templates


```html # dbcreds\web\templates\base.html
<!-- dbcreds/web/templates/base.html -->
<!DOCTYPE html>
<html lang="en" class="h-full" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ title }}{% endblock %}</title>
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- HTMX -->
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    
    <!-- Alpine.js for interactivity -->
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    
    <!-- Custom styles -->
    <link rel="stylesheet" href="/static/css/custom.css">
    
    <!-- Theme detection script -->
    <script>
        // Check for saved theme or default to system preference
        const savedTheme = localStorage.getItem('theme') || 
            (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        document.documentElement.setAttribute('data-theme', savedTheme);
    </script>
    
    <!-- Tailwind config -->
    <script>
        tailwind.config = {
            darkMode: ['class', '[data-theme="dark"]'],
            theme: {
                extend: {
                    colors: {
                        'dbcreds-blue': '#1E90FF',
                        'dbcreds-green': '#5AC85A',
                        'dbcreds-light-green': '#90EE90',
                        'dbcreds-dark-blue': '#2F3640',
                        'dbcreds-gray': '#C0C0C0',
                        'dbcreds-dark-gray': '#4B4B4B',
                        'dbcreds-teal': '#00b8a9',
                        'dbcreds-purple': '#6C5CE7',
                        'dbcreds-orange': '#FFA502',
                    }
                }
            }
        }
    </script>
    
    <style>
        [x-cloak] { display: none !important; }
    </style>
</head>
<body class="h-full transition-colors duration-300">
    <div class="min-h-full flex flex-col">
        <!-- Navigation -->
        <nav class="shadow-lg">
            <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div class="flex h-16 justify-between">
                    <div class="flex">
                        <div class="flex flex-shrink-0 items-center">
                            <img src="/static/logo.svg" alt="dbcreds" class="h-8 w-8 mr-2 rounded-lg shadow-md">
                            <h1 class="text-xl font-bold text-white">dbcreds</h1>
                            <span class="ml-3 fast-mode-indicator">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                                </svg>
                                Fast Mode
                            </span>
                        </div>
                        <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
                            <a href="/" class="text-white hover:text-gray-200 inline-flex items-center px-1 pt-1 text-sm font-medium transition-colors">
                                Environments
                            </a>
                            <a href="/settings" class="text-white hover:text-gray-200 inline-flex items-center px-1 pt-1 text-sm font-medium transition-colors">
                                Settings
                            </a>
                        </div>
                    </div>
                    <div class="flex items-center space-x-4">
                        <!-- Theme Toggle -->
                        <button onclick="toggleTheme()" class="theme-toggle" title="Toggle theme">
                            <svg class="w-5 h-5 hidden dark-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>
                            </svg>
                            <svg class="w-5 h-5 light-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>
                            </svg>
                            <span class="ml-2 hidden sm:inline">Theme</span>
                        </button>
                        <span class="text-sm text-gray-200">v{{ version }}</span>
                    </div>
                </div>
            </div>
        </nav>

        <!-- Main content -->
        <main class="flex-grow">
            <div class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
                {% block content %}{% endblock %}
            </div>
        </main>
        
        <!-- Footer -->
        <footer class="mt-auto py-4">
            <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
                <p class="text-sm">
                    Made with 💚 by <a href="https://github.com/Sunnova-ShakesDlamini" class="font-semibold hover:underline">Sunnova ShakesDlamini</a>
                </p>
                <div class="mt-2 space-x-4 text-xs">
                    <a href="https://github.com/Sunnova-ShakesDlamini/dbcreds" class="hover:underline">GitHub</a>
                    <a href="https://pypi.org/project/dbcreds/" class="hover:underline">PyPI</a>
                    <a href="https://sunnova-shakesdlamini.github.io/dbcreds/" class="hover:underline">Docs</a>
                </div>
            </div>
        </footer>
    </div>
    
    <!-- Notification container -->
    <div id="notification-container"></div>
    
    <script>
        // Theme management
        function toggleTheme() {
            const html = document.documentElement;
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcons();
        }
        
        function updateThemeIcons() {
            const theme = document.documentElement.getAttribute('data-theme');
            const darkIcon = document.querySelector('.dark-icon');
            const lightIcon = document.querySelector('.light-icon');
            
            if (theme === 'dark') {
                darkIcon.style.display = 'block';
                lightIcon.style.display = 'none';
            } else {
                darkIcon.style.display = 'none';
                lightIcon.style.display = 'block';
            }
        }
        
        // Initialize theme icons
        updateThemeIcons();
        
        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('theme')) {
                document.documentElement.setAttribute('data-theme', e.matches ? 'dark' : 'light');
                updateThemeIcons();
            }
        });
        
        // Notification system
        function showNotification(message, type = 'success', duration = 3000) {
            const container = document.getElementById('notification-container');
            
            const styles = {
                success: {
                    gradient: 'from-dbcreds-green to-green-600',
                    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>'
                },
                error: {
                    gradient: 'from-red-500 to-red-600',
                    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>'
                },
                warning: {
                    gradient: 'from-dbcreds-orange to-orange-600',
                    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>'
                },
                info: {
                    gradient: 'from-dbcreds-blue to-blue-600',
                    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>'
                }
            };
            
            const style = styles[type] || styles.success;
            
            const notification = document.createElement('div');
            notification.className = 'fixed top-4 right-4 z-50 animate-fade-in-down';
            notification.innerHTML = `
                <div class="bg-gradient-to-r ${style.gradient} text-white px-4 py-3 rounded-lg shadow-lg flex items-center space-x-3 max-w-md">
                    <svg class="h-5 w-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        ${style.icon}
                    </svg>
                    <span class="font-medium">${message}</span>
                    <button onclick="this.parentElement.parentElement.remove()" class="ml-auto -mr-1 p-1 hover:opacity-75">
                        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
            `;
            
            container.insertBefore(notification, container.firstChild);
            
            if (duration > 0) {
                setTimeout(() => {
                    if (notification.parentElement) {
                        notification.classList.add('animate-fade-out-up');
                        setTimeout(() => notification.remove(), 300);
                    }
                }, duration);
            }
        }
    </script>
</body>
</html>

```

```html # dbcreds\web\templates\index.html
<!-- dbcreds/web/templates/index.html -->
{% extends "base.html" %}

{% block content %}
<div class="px-4 sm:px-0">
    <!-- Hero Section -->
    <div class="hero-section mb-8">
        <h1 class="text-3xl font-bold mb-2">Database Environments</h1>
        <p class="text-lg opacity-90">
            Manage your database credentials securely across different environments
        </p>
    </div>
    
    <div class="sm:flex sm:items-center mb-6">
        <div class="sm:flex-auto">
            <p class="text-sm text-gray-700">
                All credentials are encrypted and stored securely in your system's credential manager.
            </p>
        </div>
        <div class="mt-4 sm:ml-16 sm:mt-0 sm:flex-none">
            <button type="button" 
                    class="btn-primary block rounded-md px-3 py-2 text-center text-sm font-semibold shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                    hx-get="/environments/new"
                    hx-target="#modal">
                Add Environment
            </button>
        </div>
    </div>
    
    <!-- Environment list -->
    <div class="card" id="environment-list" hx-get="/environments" hx-trigger="load">
        <!-- Loading state -->
        <div class="flex justify-center p-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-dbcreds-blue"></div>
        </div>
    </div>
</div>

<!-- Modal container -->
<div id="modal"></div>
{% endblock %}

```

```html # dbcreds\web\templates\partials\environment_list.html
<!-- dbcreds/web/templates/partials/environment_list.html -->
{% if environments %}
<div class="overflow-hidden shadow-lg rounded-lg">
    <table class="min-w-full">
        <thead>
            <tr>
                <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-white sm:pl-6">
                    Environment
                </th>
                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-white">
                    Type
                </th>
                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-white">
                    Description
                </th>
                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-white">
                    Password Expiry
                </th>
                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-white">
                    Status
                </th>
                <th scope="col" class="relative py-3.5 pl-3 pr-4 sm:pr-6">
                    <span class="sr-only">Actions</span>
                </th>
            </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
            {% for env in environments %}
            <tr class="hover:bg-gray-50 transition-colors">
                <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium sm:pl-6">
                    {{ env.name }}
                    {% if env.is_production %}
                    <span class="ml-2 inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium badge-danger">
                        Production
                    </span>
                    {% endif %}
                </td>
                <td class="whitespace-nowrap px-3 py-4 text-sm">
                    <span class="badge badge-info">{{ env.database_type.value }}</span>
                </td>
                <td class="whitespace-nowrap px-3 py-4 text-sm">
                    {{ env.description or "-" }}
                </td>
                <td class="whitespace-nowrap px-3 py-4 text-sm" id="expiry-{{ env.name }}">
                    <span class="inline-flex items-center">
                        <svg class="animate-spin h-4 w-4 mr-2 spinner" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Loading...
                    </span>
                </td>
                <td class="whitespace-nowrap px-3 py-4 text-sm">
                    <span class="badge badge-success">
                        Active
                    </span>
                </td>
                <td class="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                    <button hx-get="/environments/{{ env.name }}/edit" 
                            hx-target="#modal"
                            class="text-dbcreds-blue hover:text-blue-700 font-medium mr-3">
                        Edit
                    </button>
                    <button hx-post="/environments/{{ env.name }}/test" 
                            hx-target="#test-result-{{ env.name }}"
                            hx-indicator="#test-indicator-{{ env.name }}"
                            class="text-dbcreds-green hover:text-green-700 font-medium">
                        Test
                    </button>
                    <span id="test-indicator-{{ env.name }}" class="htmx-indicator ml-2">
                        <svg class="animate-spin h-4 w-4 inline spinner" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                    </span>
                    <div id="test-result-{{ env.name }}" class="mt-1"></div>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

<script>
// Load expiry information with better error handling
function loadExpiryInfo(envName) {
    fetch("/api/environments/" + envName + "/expiry")
        .then(response => response.json())
        .then(data => {
            const element = document.getElementById("expiry-" + envName);
            if (!element) return;
            
            let html = '';
            let badgeClass = '';
            
            if (data.error) {
                html = '<span class="badge bg-gray-500 text-white">Error</span>';
            } else if (data.is_expired) {
                html = '<span class="badge badge-danger">Expired</span>';
            } else if (data.days_left !== null) {
                if (data.days_left <= 7) {
                    badgeClass = 'badge-danger';
                } else if (data.days_left <= 30) {
                    badgeClass = 'badge-warning';
                } else {
                    badgeClass = 'badge-success';
                }
                html = `<span class="badge ${badgeClass}">${data.days_left} days left</span>`;
            } else if (data.updated_at && !data.has_expiry) {
                html = '<span class="badge bg-gray-500 text-white">Not tracked</span>';
            } else {
                html = '<span class="badge bg-gray-500 text-white">No expiry</span>';
            }
            
            element.innerHTML = html;
        })
        .catch(error => {
            console.error("Error loading expiry:", error);
            const element = document.getElementById("expiry-" + envName);
            if (element) {
                element.innerHTML = '<span class="badge bg-gray-500 text-white">Error</span>';
            }
        });
}

// Load all expiry info
function loadAllExpiryInfo() {
    {% for env in environments %}
    loadExpiryInfo("{{ env.name }}");
    {% endfor %}
}

// Initial load
document.addEventListener("DOMContentLoaded", loadAllExpiryInfo);
loadAllExpiryInfo();
</script>
{% else %}
<!-- Empty state -->
<div class="card text-center py-12">
    <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path>
    </svg>
    <p class="text-gray-500 mb-4">No environments configured yet.</p>
    <button type="button" 
            class="btn-primary mx-auto"
            hx-get="/environments/new"
            hx-target="#modal">
        Add Your First Environment
    </button>
</div>
{% endif %}

```

```html # dbcreds\web\templates\settings.html
<!-- dbcreds/web/templates/settings.html -->
{% extends "base.html" %}

{% block content %}
<div class="px-4 sm:px-0">
    <div class="pb-5 border-b border-gray-200">
        <h1 class="text-2xl font-semibold leading-6 text-gray-900">Settings</h1>
        <p class="mt-2 text-sm text-gray-700">
            Configure dbcreds behavior and preferences.
        </p>
    </div>

    <!-- Settings sections -->
    <div class="mt-6 space-y-8">
        
        <!-- General Settings -->
        <div class="card">
            <div class="px-4 py-5 sm:p-6">
                <h3 class="text-lg font-medium leading-6 text-gray-900">General Settings</h3>
                <div class="mt-2 max-w-xl text-sm text-gray-500">
                    <p>Configure general application behavior.</p>
                </div>
                <div class="mt-5 space-y-4">
                    <div class="flex items-center justify-between">
                        <div>
                            <label class="text-sm font-medium text-gray-900">Configuration Directory</label>
                            <p class="text-sm text-gray-500">{{ config_dir }}</p>
                        </div>
                    </div>
                    <div class="flex items-center justify-between">
                        <div>
                            <label class="text-sm font-medium text-gray-900">Default Password Expiry</label>
                            <p class="text-sm text-gray-500">90 days</p>
                        </div>
                        <button type="button" class="text-sm text-dbcreds-blue hover:text-blue-700">
                            Change
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Backend Information -->
        <div class="card">
            <div class="px-4 py-5 sm:p-6">
                <h3 class="text-lg font-medium leading-6 text-gray-900">Storage Backends</h3>
                <div class="mt-2 max-w-xl text-sm text-gray-500">
                    <p>Available credential storage backends on this system.</p>
                </div>
                <div class="mt-5">
                    <ul class="divide-y divide-gray-200">
                        {% for backend in backends %}
                        <li class="py-3 flex justify-between items-center">
                            <div>
                                <p class="text-sm font-medium text-gray-900">{{ backend.name }}</p>
                                <p class="text-sm text-gray-500">{{ backend.description }}</p>
                            </div>
                            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {% if backend.available %}badge-success{% else %}bg-gray-100 text-gray-800{% endif %}">
                                {% if backend.available %}Available{% else %}Not Available{% endif %}
                            </span>
                        </li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
        </div>

        <!-- Security Settings -->
        <div class="card">
            <div class="px-4 py-5 sm:p-6">
                <h3 class="text-lg font-medium leading-6 text-gray-900">Security</h3>
                <div class="mt-2 max-w-xl text-sm text-gray-500">
                    <p>Configure security-related settings.</p>
                </div>
                <div class="mt-5 space-y-4">
                    <div class="flex items-start">
                        <div class="flex items-center h-5">
                            <input id="warn-expiry" name="warn-expiry" type="checkbox" checked 
                                   class="focus:ring-dbcreds-blue h-4 w-4 text-dbcreds-blue border-gray-300 rounded">
                        </div>
                        <div class="ml-3 text-sm">
                            <label for="warn-expiry" class="font-medium text-gray-700">Password expiry warnings</label>
                            <p class="text-gray-500">Show warnings when passwords are about to expire.</p>
                        </div>
                    </div>
                    <div class="flex items-start">
                        <div class="flex items-center h-5">
                            <input id="auto-lock" name="auto-lock" type="checkbox" 
                                   class="focus:ring-dbcreds-blue h-4 w-4 text-dbcreds-blue border-gray-300 rounded">
                        </div>
                        <div class="ml-3 text-sm">
                            <label for="auto-lock" class="font-medium text-gray-700">Auto-lock credentials</label>
                            <p class="text-gray-500">Require re-authentication after period of inactivity.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Export/Import -->
        <div class="card">
            <div class="px-4 py-5 sm:p-6">
                <h3 class="text-lg font-medium leading-6 text-gray-900">Export & Import</h3>
                <div class="mt-2 max-w-xl text-sm text-gray-500">
                    <p>Export environment configurations or import from backup.</p>
                </div>
                <div class="mt-5 flex space-x-3">
                    <button type="button" class="btn-secondary inline-flex items-center px-4 py-2 shadow-sm text-sm font-medium rounded-md">
                        <svg class="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
                        </svg>
                        Export Configuration
                    </button>
                    <button type="button" class="btn-secondary inline-flex items-center px-4 py-2 shadow-sm text-sm font-medium rounded-md">
                        <svg class="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                        </svg>
                        Import Configuration
                    </button>
                </div>
            </div>
        </div>

        <!-- Danger Zone -->
        <div class="card bg-red-50 border-red-200">
            <div class="px-4 py-5 sm:p-6">
                <h3 class="text-lg font-medium leading-6 text-red-900">Danger Zone</h3>
                <div class="mt-2 max-w-xl text-sm text-red-700">
                    <p>Irreversible actions that affect all stored credentials.</p>
                </div>
                <div class="mt-5">
                    <button type="button" class="inline-flex items-center justify-center px-4 py-2 border border-transparent font-medium rounded-md text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:text-sm">
                        Clear All Credentials
                    </button>
                </div>
            </div>
        </div>

    </div>
</div>
{% endblock %}

```


## Export Fast.Py


```python # dbcreds\export_fast.py
# dbcreds/export_fast.py
"""
Script to export the fast credential access as a standalone module.

Usage:
    python -m dbcreds.export_fast [output_path]
"""

import sys
from pathlib import Path
from typing import Optional  # Add this import!

FAST_MODULE_CODE = '''"""
Fast database credential access - standalone module.

This module is auto-generated from dbcreds for use in environments
where importing the full dbcreds package causes issues (e.g., marimo notebooks).

Generated from dbcreds version: {version}
Generated on: {date}
"""

import os
import ctypes
import ctypes.wintypes
import json
from typing import Dict, Any, Optional
from functools import lru_cache


@lru_cache(maxsize=10)
def get_connection_string(environment: str) -> str:
    """
    Get database connection string using fast, lightweight method.
    
    This bypasses all dbcreds initialization and directly reads from
    environment variables or Windows Credential Manager.
    
    Args:
        environment: Environment name
        
    Returns:
        Database connection URI
        
    Raises:
        ValueError: If credentials not found
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
        f"No credentials found for environment '{{environment}}'. "
        "Please ensure credentials are set in environment variables or Windows Credential Manager."
    )


def _get_from_environment(env_name: str) -> Optional[str]:
    """Try to get connection from environment variables."""
    # Check if dbcreds has set environment variables
    prefix = f"DBCREDS_{{env_name.upper()}}_"
    
    # Also check legacy format (for PowerShell compatibility)
    legacy_vars = {{
        'host': os.environ.get('DB_SERVER'),
        'port': os.environ.get('DB_PORT', '5432'),
        'database': os.environ.get('DB_NAME'),
        'username': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PWD'),
    }}
    
    # Check new format
    new_vars = {{
        'host': os.environ.get(f'{{prefix}}HOST'),
        'port': os.environ.get(f'{{prefix}}PORT', '5432'),
        'database': os.environ.get(f'{{prefix}}DATABASE'),
        'username': os.environ.get(f'{{prefix}}USERNAME'),
        'password': os.environ.get(f'{{prefix}}PASSWORD'),
    }}
    
    # Use whichever has data
    vars_to_use = new_vars if new_vars['host'] else legacy_vars
    
    if all(vars_to_use.get(k) for k in ['host', 'database', 'username']):
        # Password might be in credential manager, but try env first
        if not vars_to_use.get('password') and os.name == 'nt':
            # Try to get from Windows Credential Manager
            cred_data = _read_windows_credential(f"dbcreds:{{env_name}}")
            if cred_data and cred_data.get('password'):
                vars_to_use['password'] = cred_data['password']
        
        if vars_to_use.get('password'):
            return (
                f"postgresql://{{vars_to_use['username']}}:{{vars_to_use['password']}}"
                f"@{{vars_to_use['host']}}:{{vars_to_use['port']}}/{{vars_to_use['database']}}"
            )
    
    return None


def _get_from_windows_credential_manager(env_name: str) -> Optional[str]:
    """Get connection string from Windows Credential Manager."""
    if os.name != 'nt':
        return None
    
    cred_data = _read_windows_credential(f"dbcreds:{{env_name}}")
    if cred_data and all(k in cred_data for k in ['username', 'password', 'host', 'database']):
        return (
            f"postgresql://{{cred_data['username']}}:{{cred_data['password']}}"
            f"@{{cred_data['host']}}:{{cred_data.get('port', 5432)}}/{{cred_data['database']}}"
        )
    
    return None


def _read_windows_credential(target: str) -> Dict[str, Any]:
    """Read credential from Windows Credential Manager using ctypes."""
    if os.name != 'nt':
        return {{}}
    
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
                    return {{
                        'username': username,
                        'password': password,
                        'host': data.get('host', ''),
                        'port': data.get('port', 5432),
                        'database': data.get('database', ''),
                    }}
                except (json.JSONDecodeError, UnicodeDecodeError):
                    # Fallback: treat entire blob as password
                    password = blob_data.decode('utf-16le', errors='ignore').rstrip('\\x00')
                    return {{
                        'username': username,
                        'password': password
                    }}
            
            return {{'username': username, 'password': ''}}
            
        finally:
            advapi32.CredFree(cred_ptr)
    
    return {{}}


# Convenience functions for different database types
def get_postgresql_connection_string(environment: str) -> str:
    """Get PostgreSQL connection string."""
    return get_connection_string(environment)


def get_mysql_connection_string(environment: str) -> str:
    """Get MySQL connection string."""
    conn_string = get_connection_string(environment)
    # Convert postgresql:// to mysql://
    if conn_string.startswith('postgresql://'):
        return 'mysql://' + conn_string[13:]
    return conn_string


def get_mssql_connection_string(environment: str) -> str:
    """Get SQL Server connection string."""
    conn_string = get_connection_string(environment)
    # Convert to SQL Server format
    if conn_string.startswith('postgresql://'):
        base = conn_string[13:]
        return f'mssql+pyodbc://{{base}}?driver=ODBC+Driver+17+for+SQL+Server'
    return conn_string


# Aliases for convenience
get = get_connection_string
get_postgres = get_postgresql_connection_string
get_mysql = get_mysql_connection_string
get_mssql = get_mssql_connection_string
'''


def export_fast_module(output_path: Optional[str] = None):
    """Export the fast module as a standalone file."""
    from datetime import datetime

    # Try to get version, but don't fail if can't import
    try:
        from dbcreds import __version__

        version = __version__
    except:
        version = "unknown"

    # Determine output path
    if output_path is None:
        # Default to current directory
        output_path = "dbcreds_fast.py"

    output_file = Path(output_path)

    # Create directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Format the code with metadata
    code = FAST_MODULE_CODE.format(
        version=version, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    # Write the file
    output_file.write_text(code)

    print(f"✅ Fast module exported to: {output_file.absolute()}")
    print(f"📝 File size: {len(code):,} bytes")
    print("\nUsage in marimo or any Python script:")
    print("    from dbcreds_fast import get_connection_string")
    print("    conn_string = get_connection_string('your_environment')")

    return str(output_file.absolute())


def main():
    """Main entry point for the export script."""
    output_path = sys.argv[1] if len(sys.argv) > 1 else None
    export_fast_module(output_path)


if __name__ == "__main__":
    main()

```


## Fast.Py


```python # dbcreds\fast.py
# dbcreds/fast.py
"""
Fast, lightweight credential access for environments like marimo notebooks.

This module provides direct credential access without initializing the full
dbcreds infrastructure.
"""

import os
import ctypes
import ctypes.wintypes
import json
from typing import Dict, Any, Optional


def get_connection_string(environment: str) -> str:
    """
    Get database connection string using fast, lightweight method.
    
    This bypasses all dbcreds initialization and directly reads from
    environment variables or Windows Credential Manager.
    
    Args:
        environment: Environment name
        
    Returns:
        Database connection URI
        
    Raises:
        ValueError: If credentials not found
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


# Convenience aliases
get = get_connection_string
fast_get = get_connection_string
```