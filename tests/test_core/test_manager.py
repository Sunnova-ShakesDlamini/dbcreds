# tests/test_core/test_manager.py
"""Tests for the CredentialManager class."""

import tempfile
from datetime import datetime, timedelta, timezone

import pytest

from dbcreds.backends.base import CredentialBackend
from dbcreds.core.exceptions import (
    CredentialError,
    CredentialNotFoundError,
    PasswordExpiredError,
)
from dbcreds.core.manager import CredentialManager
from dbcreds.core.models import DatabaseType


class MockBackend(CredentialBackend):
    """Mock backend for testing."""

    def __init__(self):
        self.storage = {}

    def is_available(self) -> bool:
        return True

    def get_credential(self, key: str):
        return self.storage.get(key)

    def set_credential(
        self, key: str, username: str, password: str, metadata: dict
    ) -> bool:
        self.storage[key] = (username, password, metadata)
        return True

    def delete_credential(self, key: str) -> bool:
        if key in self.storage:
            del self.storage[key]
            return True
        return False


@pytest.fixture
def temp_config_dir():
    """Create a temporary config directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def mock_backend():
    """Create a mock backend."""
    return MockBackend()


@pytest.fixture
def manager(temp_config_dir, mock_backend):
    """Create a CredentialManager with mocked backends."""
    # Create manager with temp config dir
    manager = CredentialManager(config_dir=temp_config_dir)
    # Clear any backends that were auto-initialized
    manager.backends = []
    # Add only our mock backend
    manager.backends.append(mock_backend)
    return manager


@pytest.fixture
def sample_credentials():
    """Sample credential data for testing."""
    return {
        "host": "localhost",
        "port": 5432,
        "database": "testdb",
        "username": "testuser",
        "password": "testpass123",
    }


class TestCredentialManager:
    """Test cases for CredentialManager."""

    def test_add_environment(self, manager):
        """Test adding a new environment."""
        env = manager.add_environment(
            "test-env", DatabaseType.POSTGRESQL, "Test environment"
        )

        assert env.name == "test-env"
        assert env.database_type == DatabaseType.POSTGRESQL
        assert env.description == "Test environment"
        assert not env.is_production

        # Verify environment is stored
        assert "test-env" in manager.environments

    def test_add_duplicate_environment(self, manager):
        """Test adding a duplicate environment raises error."""
        manager.add_environment("test-env", DatabaseType.POSTGRESQL)

        with pytest.raises(CredentialError, match="already exists"):
            manager.add_environment("test-env", DatabaseType.MYSQL)

    def test_set_and_get_credentials(self, manager, sample_credentials):
        """Test storing and retrieving credentials."""
        # Add environment
        manager.add_environment("test-env", DatabaseType.POSTGRESQL)

        # Set credentials
        creds = manager.set_credentials("test-env", **sample_credentials)

        assert creds.host == sample_credentials["host"]
        assert creds.port == sample_credentials["port"]
        assert creds.database == sample_credentials["database"]
        assert creds.username == sample_credentials["username"]

        # Get credentials
        retrieved = manager.get_credentials("test-env")
        assert retrieved.host == sample_credentials["host"]
        assert retrieved.port == sample_credentials["port"]
        assert retrieved.database == sample_credentials["database"]
        assert retrieved.username == sample_credentials["username"]
        assert retrieved.password.get_secret_value() == sample_credentials["password"]

    def test_get_nonexistent_credentials(self, manager):
        """Test getting credentials for nonexistent environment."""
        with pytest.raises(CredentialNotFoundError):
            manager.get_credentials("nonexistent")

    def test_password_expiry(self, manager, sample_credentials):
        """Test password expiry functionality."""
        manager.add_environment("test-env", DatabaseType.POSTGRESQL)

        # Set credentials with already expired password
        # First set normal credentials
        manager.set_credentials(
            "test-env", **sample_credentials, password_expires_days=90
        )

        # Now manually update the backend storage to have expired credentials
        mock_backend = manager.backends[0]

        # Get the current stored data
        username, password, metadata = mock_backend.storage["dbcreds:test-env"]

        # Update the expiry date to be in the past
        expired_date = datetime.now(timezone.utc) - timedelta(days=1)
        metadata["password_expires_at"] = expired_date.isoformat()

        # Store back with updated metadata
        mock_backend.storage["dbcreds:test-env"] = (username, password, metadata)

        # Should raise password expired error
        with pytest.raises(PasswordExpiredError):
            manager.get_credentials("test-env")

    def test_password_expiry_disabled(self, manager, sample_credentials):
        """Test credentials with no expiry."""
        manager.add_environment("test-env", DatabaseType.POSTGRESQL)

        # Set credentials without expiry
        manager.set_credentials(
            "test-env", **sample_credentials, password_expires_days=None
        )

        # Should not raise error
        creds = manager.get_credentials("test-env")
        assert creds.password_expires_at is None
        assert not creds.is_password_expired()

    def test_remove_environment(self, manager, sample_credentials):
        """Test removing an environment."""
        manager.add_environment("test-env", DatabaseType.POSTGRESQL)
        manager.set_credentials("test-env", **sample_credentials)

        # Verify it exists
        assert "test-env" in manager.environments

        # Remove it
        manager.remove_environment("test-env")

        # Verify it's gone
        assert "test-env" not in manager.environments

        # Verify credentials are also gone
        with pytest.raises(CredentialNotFoundError):
            manager.get_credentials("test-env")

    def test_list_environments(self, manager):
        """Test listing environments."""
        # Add multiple environments
        manager.add_environment("dev", DatabaseType.POSTGRESQL)
        manager.add_environment("staging", DatabaseType.MYSQL)
        manager.add_environment("prod", DatabaseType.POSTGRESQL, is_production=True)

        envs = manager.list_environments()
        assert len(envs) == 3

        env_names = [env.name for env in envs]
        assert "dev" in env_names
        assert "staging" in env_names
        assert "prod" in env_names

        # Check production flag
        prod_env = next(env for env in envs if env.name == "prod")
        assert prod_env.is_production
