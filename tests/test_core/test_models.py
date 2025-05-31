# tests/test_core/test_models.py
"""Tests for Pydantic models."""

from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from dbcreds.core.models import DatabaseCredentials, DatabaseType, Environment


class TestEnvironment:
    """Test cases for Environment model."""

    def test_create_environment(self):
        """Test creating a valid environment."""
        env = Environment(
            name="test-env",
            database_type=DatabaseType.POSTGRESQL,
            description="Test environment",
            is_production=False,
        )

        assert env.name == "test-env"
        assert env.database_type == DatabaseType.POSTGRESQL
        assert env.description == "Test environment"
        assert not env.is_production
        assert isinstance(env.created_at, datetime)
        assert isinstance(env.updated_at, datetime)

    def test_environment_name_validation(self):
        """Test environment name validation."""
        # Valid names
        for name in ["dev", "test-env", "prod_db", "env123"]:
            env = Environment(name=name, database_type=DatabaseType.POSTGRESQL)
            assert env.name == name.lower()

        # Invalid names
        with pytest.raises(ValidationError):
            Environment(
                name="test env", database_type=DatabaseType.POSTGRESQL
            )  # spaces

        with pytest.raises(ValidationError):
            Environment(
                name="test@env", database_type=DatabaseType.POSTGRESQL
            )  # special chars

    def test_environment_name_lowercase(self):
        """Test that environment names are converted to lowercase."""
        env = Environment(name="TEST-ENV", database_type=DatabaseType.POSTGRESQL)
        assert env.name == "test-env"


class TestDatabaseCredentials:
    """Test cases for DatabaseCredentials model."""

    def test_create_credentials(self):
        """Test creating valid credentials."""
        creds = DatabaseCredentials(
            environment="test",
            host="localhost",
            port=5432,
            database="testdb",
            username="user",
            password="pass123",
        )

        assert creds.environment == "test"
        assert creds.host == "localhost"
        assert creds.port == 5432
        assert creds.database == "testdb"
        assert creds.username == "user"
        assert creds.password.get_secret_value() == "pass123"
        assert isinstance(creds.password_updated_at, datetime)

    def test_port_validation(self):
        """Test port number validation."""
        # Valid ports
        for port in [1, 80, 443, 5432, 65535]:
            creds = DatabaseCredentials(
                environment="test",
                host="localhost",
                port=port,
                database="testdb",
                username="user",
                password="pass",
            )
            assert creds.port == port

        # Invalid ports
        with pytest.raises(ValidationError):
            DatabaseCredentials(
                environment="test",
                host="localhost",
                port=0,  # too low
                database="testdb",
                username="user",
                password="pass",
            )

        with pytest.raises(ValidationError):
            DatabaseCredentials(
                environment="test",
                host="localhost",
                port=65536,  # too high
                database="testdb",
                username="user",
                password="pass",
            )

    def test_password_expiry(self):
        """Test password expiry functionality."""
        # Not expired
        expires_at = datetime.now(timezone.utc) + timedelta(days=30)
        creds = DatabaseCredentials(
            environment="test",
            host="localhost",
            port=5432,
            database="testdb",
            username="user",
            password="pass",
            password_expires_at=expires_at,
        )

        assert not creds.is_password_expired()
        days_left = creds.days_until_expiry()
        assert 29 <= days_left <= 30  # Allow for slight timing differences

        # Expired
        expired_at = datetime.now(timezone.utc) - timedelta(days=1)
        creds = DatabaseCredentials(
            environment="test",
            host="localhost",
            port=5432,
            database="testdb",
            username="user",
            password="pass",
            password_expires_at=expired_at,
        )

        assert creds.is_password_expired()
        assert creds.days_until_expiry() == 0

        # No expiry
        creds = DatabaseCredentials(
            environment="test",
            host="localhost",
            port=5432,
            database="testdb",
            username="user",
            password="pass",
            password_expires_at=None,
        )

        assert not creds.is_password_expired()
        assert creds.days_until_expiry() is None

    def test_connection_string(self):
        """Test connection string generation."""
        creds = DatabaseCredentials(
            environment="test",
            host="localhost",
            port=5432,
            database="testdb",
            username="user",
            password="pass123",
        )

        # With password
        conn_str = creds.get_connection_string(include_password=True)
        assert conn_str == "postgresql://user:pass123@localhost:5432/testdb"

        # Without password
        conn_str = creds.get_connection_string(include_password=False)
        assert conn_str == "postgresql://user@localhost:5432/testdb"
