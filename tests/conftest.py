# tests/conftest.py
"""Shared test fixtures."""

import tempfile

import pytest
from fastapi.testclient import TestClient

from dbcreds.core.manager import CredentialManager
from dbcreds.web.main import app


@pytest.fixture
def temp_config_dir():
    """Create a temporary configuration directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def manager(temp_config_dir):
    """Create a credential manager with temporary storage."""
    return CredentialManager(config_dir=temp_config_dir)


@pytest.fixture
def test_client():
    """Create a test client for the web interface."""
    return TestClient(app)


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
