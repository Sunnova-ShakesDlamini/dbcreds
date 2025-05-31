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