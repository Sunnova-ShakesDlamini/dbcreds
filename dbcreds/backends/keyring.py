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
