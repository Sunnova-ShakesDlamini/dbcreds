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