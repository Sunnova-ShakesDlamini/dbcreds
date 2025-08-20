#!/usr/bin/env python3
"""
Add security features, tests, documentation, and examples to dbcreds package.
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
import argparse

# ANSI color codes for output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.CYAN}ℹ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_header(message):
    print(f"\n{Colors.YELLOW}{message}{Colors.END}")
    print("-" * 40)

def write_file(path, content):
    """Write content to file, creating directories as needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

def create_backup(project_path):
    """Create a backup of the project."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = f"backup_{timestamp}"
    
    print_info("Creating backup of current project...")
    
    # Copy everything except certain directories
    ignore_patterns = shutil.ignore_patterns(
        '.git', '__pycache__', '*.pyc', '.pytest_cache', 'backup_*', 
        '*.egg-info', '.coverage', 'htmlcov', 'site'
    )
    
    shutil.copytree(project_path, backup_dir, ignore=ignore_patterns)
    print_success(f"Backup created: {backup_dir}")
    return backup_dir

def add_security_features():
    """Add security features to the project."""
    print_header("📔 Adding Security Features")
    
    # Create auth.py for web interface
    print_info("Creating web authentication module...")
    auth_content = '''# dbcreds/web/auth.py
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
'''
    
    write_file("dbcreds/web/auth.py", auth_content)
    print_success("Created dbcreds/web/auth.py")
    
    # Create security.py for core
    print_info("Creating core security module...")
    security_content = '''# dbcreds/core/security.py
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
        masked = re.sub(pattern, r"\\1****\\3", masked, flags=re.IGNORECASE)
    
    return masked
'''
    
    write_file("dbcreds/core/security.py", security_content)
    print_success("Created dbcreds/core/security.py")
    
    # Update web/main.py with security middleware
    print_info("Updating web/main.py with security features...")
    main_py_path = Path("dbcreds/web/main.py")
    if main_py_path.exists():
        content = main_py_path.read_text()
        
        # Add imports if not present
        if "from fastapi.middleware.cors import CORSMiddleware" not in content:
            import_insert = """from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware"""
            content = content.replace("from fastapi import", f"{import_insert}\nfrom fastapi import")
        
        # Add middleware after app creation if not present
        if "app.add_middleware(" not in content:
            middleware_insert = '''
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
'''
            # Find position after app creation
            app_pattern = r"(app = FastAPI\([^)]+\))"
            content = re.sub(app_pattern, f"\\1{middleware_insert}", content)
        
        write_file("dbcreds/web/main.py", content)
        print_success("Updated dbcreds/web/main.py with security middleware")

def create_test_suite():
    """Create test suite structure and files."""
    print_header("🧪 Creating Test Suite")
    
    # Create test directories
    test_dirs = [
        "tests",
        "tests/test_core",
        "tests/test_backends",
        "tests/test_cli",
        "tests/test_web"
    ]
    
    for dir_path in test_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        (Path(dir_path) / "__init__.py").touch()
    
    print_success("Created test directory structure")
    
    # Create conftest.py
    print_info("Creating test fixtures...")
    conftest_content = '''# tests/conftest.py
"""Shared test fixtures."""

import os
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from dbcreds.core.manager import CredentialManager
from dbcreds.core.models import DatabaseType
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
'''
    
    write_file("tests/conftest.py", conftest_content)
    print_success("Created tests/conftest.py")
    
    # Create test_manager.py
    print_info("Creating manager tests...")
    test_manager_content = '''# tests/test_core/test_manager.py
"""Tests for the credential manager."""

import pytest

from dbcreds.core.exceptions import CredentialError, CredentialNotFoundError
from dbcreds.core.models import DatabaseType


class TestCredentialManager:
    """Test credential manager functionality."""
    
    def test_add_environment(self, manager):
        """Test adding a new environment."""
        env = manager.add_environment(
            "test-env",
            DatabaseType.POSTGRESQL,
            "Test environment",
            is_production=False
        )
        
        assert env.name == "test-env"
        assert env.database_type == DatabaseType.POSTGRESQL
        assert env.description == "Test environment"
        assert not env.is_production
    
    def test_add_duplicate_environment(self, manager):
        """Test adding duplicate environment raises error."""
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
        assert retrieved.password.get_secret_value() == sample_credentials["password"]
    
    def test_get_nonexistent_credentials(self, manager):
        """Test getting credentials for nonexistent environment."""
        with pytest.raises(CredentialNotFoundError):
            manager.get_credentials("nonexistent")
    
    def test_password_expiry(self, manager, sample_credentials):
        """Test password expiry functionality."""
        manager.add_environment("test-env", DatabaseType.POSTGRESQL)
        
        # Set credentials with 0 days expiry
        manager.set_credentials("test-env", **sample_credentials, password_expires_days=0)
        
        # Should raise password expired error
        from dbcreds.core.exceptions import PasswordExpiredError
        with pytest.raises(PasswordExpiredError):
            manager.get_credentials("test-env", check_expiry=True)
    
    def test_remove_environment(self, manager, sample_credentials):
        """Test removing an environment."""
        manager.add_environment("test-env", DatabaseType.POSTGRESQL)
        manager.set_credentials("test-env", **sample_credentials)
        
        # Remove environment
        manager.remove_environment("test-env")
        
        # Should not exist anymore
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
'''
    
    write_file("tests/test_core/test_manager.py", test_manager_content)
    print_success("Created tests/test_core/test_manager.py")
    
    # Create test_models.py
    print_info("Creating model tests...")
    test_models_content = '''# tests/test_core/test_models.py
"""Tests for data models."""

from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from dbcreds.core.models import DatabaseCredentials, DatabaseType, Environment


class TestEnvironmentModel:
    """Test Environment model."""
    
    def test_valid_environment(self):
        """Test creating a valid environment."""
        env = Environment(
            name="test-env",
            database_type=DatabaseType.POSTGRESQL,
            description="Test environment"
        )
        
        assert env.name == "test-env"
        assert env.database_type == DatabaseType.POSTGRESQL
        assert env.description == "Test environment"
        assert not env.is_production
    
    def test_invalid_environment_name(self):
        """Test environment name validation."""
        with pytest.raises(ValidationError):
            Environment(
                name="test env with spaces",
                database_type=DatabaseType.POSTGRESQL
            )
    
    def test_environment_name_lowercase(self):
        """Test environment name is converted to lowercase."""
        env = Environment(
            name="TEST-ENV",
            database_type=DatabaseType.POSTGRESQL
        )
        assert env.name == "test-env"


class TestDatabaseCredentials:
    """Test DatabaseCredentials model."""
    
    def test_valid_credentials(self):
        """Test creating valid credentials."""
        creds = DatabaseCredentials(
            environment="test",
            host="localhost",
            port=5432,
            database="testdb",
            username="user",
            password="pass123"
        )
        
        assert creds.host == "localhost"
        assert creds.port == 5432
        assert creds.password.get_secret_value() == "pass123"
    
    def test_invalid_port(self):
        """Test port validation."""
        with pytest.raises(ValidationError):
            DatabaseCredentials(
                environment="test",
                host="localhost",
                port=99999,  # Invalid port
                database="testdb",
                username="user",
                password="pass123"
            )
    
    def test_password_expiry(self):
        """Test password expiry calculation."""
        # Create credentials with expiry
        expires_at = datetime.utcnow() + timedelta(days=30)
        creds = DatabaseCredentials(
            environment="test",
            host="localhost",
            port=5432,
            database="testdb",
            username="user",
            password="pass123",
            password_expires_at=expires_at
        )
        
        assert not creds.is_password_expired()
        assert creds.days_until_expiry() == 29  # Approximately
        
        # Create expired credentials
        expired_at = datetime.utcnow() - timedelta(days=1)
        expired_creds = DatabaseCredentials(
            environment="test",
            host="localhost",
            port=5432,
            database="testdb",
            username="user",
            password="pass123",
            password_expires_at=expired_at
        )
        
        assert expired_creds.is_password_expired()
        assert expired_creds.days_until_expiry() == 0
    
    def test_connection_string(self):
        """Test connection string generation."""
        creds = DatabaseCredentials(
            environment="test",
            host="localhost",
            port=5432,
            database="testdb",
            username="user",
            password="pass123"
        )
        
        # With password
        conn_str = creds.get_connection_string(include_password=True)
        assert "pass123" in conn_str
        assert "user" in conn_str
        assert "localhost:5432" in conn_str
        
        # Without password
        conn_str_no_pwd = creds.get_connection_string(include_password=False)
        assert "pass123" not in conn_str_no_pwd
        assert "user" in conn_str_no_pwd
'''
    
    write_file("tests/test_core/test_models.py", test_models_content)
    print_success("Created tests/test_core/test_models.py")
    
    # Create pytest.ini
    print_info("Creating pytest configuration...")
    pytest_ini = '''[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --strict-markers
    --tb=short
    --cov=dbcreds
    --cov-report=html
    --cov-report=term-missing:skip-covered
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
'''
    
    write_file("pytest.ini", pytest_ini)
    print_success("Created pytest.ini")

def create_documentation():
    """Create documentation structure and files."""
    print_header("📚 Creating Documentation")
    
    # Create docs directories
    doc_dirs = [
        "docs",
        "docs/getting-started",
        "docs/guide",
        "docs/examples",
        "docs/security",
        "docs/api"
    ]
    
    for dir_path in doc_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print_success("Created documentation directory structure")
    
    # Create mkdocs.yml
    print_info("Creating MkDocs configuration...")
    mkdocs_content = '''# mkdocs.yml
site_name: dbcreds Documentation
site_description: Professional database credentials management
site_author: Your Company
site_url: https://yourcompany.github.io/dbcreds

repo_name: yourcompany/dbcreds
repo_url: https://github.com/yourcompany/dbcreds

theme:
  name: material
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
    - search.suggest
    - search.highlight
    - content.code.annotate
    - content.code.copy

plugins:
  - search
  - mkdocstrings:
      default_handler: python
      handlers:
        python:
          options:
            show_source: true
            show_root_heading: true
            show_root_toc_entry: true
            show_object_full_path: false
            show_category_heading: true
            show_if_no_docstring: false

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.tabbed:
      alternate_style: true
  - attr_list
  - md_in_html
  - toc:
      permalink: true

nav:
  - Home: index.md
  - Getting Started:
    - Installation: getting-started/installation.md
    - Quick Start: getting-started/quickstart.md
    - Configuration: getting-started/configuration.md
  - User Guide:
    - CLI Usage: guide/cli.md
    - Python API: guide/python-api.md
    - Web Interface: guide/web-interface.md
    - Migration: guide/migration.md
  - Examples:
    - Basic Usage: examples/basic.md
    - SQLAlchemy: examples/sqlalchemy.md
    - Pandas: examples/pandas.md
    - Async: examples/async.md
  - Security:
    - Best Practices: security/best-practices.md
    - Backend Security: security/backends.md
  - API Reference:
    - Core: api/core.md
    - Backends: api/backends.md
    - CLI: api/cli.md
    - Web: api/web.md

extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/yourcompany
    - icon: fontawesome/brands/twitter
      link: https://twitter.com/yourcompany
'''
    
    write_file("mkdocs.yml", mkdocs_content)
    print_success("Created mkdocs.yml")
    
    # Create docs/index.md
    print_info("Creating documentation homepage...")
    docs_index = '''# dbcreds

Professional database credentials management with security and team collaboration in mind.

## Features

- **Secure Storage**: Multiple backend support (Windows Credential Manager, macOS Keychain, Linux Secret Service)
- **Multi-Environment**: Manage credentials for development, staging, and production
- **Rich CLI**: Beautiful command-line interface with Rich and Typer
- **Web UI**: Optional FastAPI web interface with HTMX
- **Multi-Database**: Support for PostgreSQL, MySQL, Oracle, SQL Server
- **Password Rotation**: Track password age and expiration
- **Full Documentation**: Comprehensive docs with mkdocstrings
- **Type Safety**: Pydantic models for validation

## Quick Example

```python
from dbcreds import get_engine
import pandas as pd

# Get a SQLAlchemy engine for your environment
engine = get_engine("production")

# Use it with pandas
df = pd.read_sql("SELECT * FROM users LIMIT 10", engine)
print(df.head())
```

## Why dbcreds?

Managing database credentials securely across multiple environments is challenging:

- **Security**: Credentials should never be stored in plain text
- **Convenience**: Developers need easy access to credentials
- **Rotation**: Passwords need regular updates
- **Team Collaboration**: Teams need to share credentials safely

dbcreds solves these problems with a professional, secure approach to credential management.

## Getting Started

Check out the [Quick Start Guide](getting-started/quickstart.md) to get up and running in minutes!
'''
    
    write_file("docs/index.md", docs_index)
    print_success("Created docs/index.md")
    
    # Create quickstart guide
    print_info("Creating quick start guide...")
    quickstart = '''# Quick Start Guide

Get started with dbcreds in just a few minutes!

## Installation

```bash
pip install git+https://github.com/yourcompany/dbcreds.git
```

## Initialize dbcreds

```bash
dbcreds init
```

This creates the configuration directory and checks available backends.

## Add Your First Environment

```bash
dbcreds add dev --type postgresql
```

You'll be prompted for:
- Database host
- Port (defaults to 5432 for PostgreSQL)
- Database name
- Username
- Password

## Use in Python

```python
from dbcreds import get_connection
import pandas as pd

# Get a connection
with get_connection("dev") as conn:
    df = pd.read_sql("SELECT * FROM my_table LIMIT 10", conn)
    print(df.head())
```

## Using with SQLAlchemy

```python
from dbcreds import get_engine
from sqlalchemy.orm import sessionmaker

# Get an engine
engine = get_engine("dev")

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Use the session
results = session.execute("SELECT 1")
print(results.scalar())
```

## Check Password Expiry

```bash
dbcreds check
```

This shows you which passwords are expired or expiring soon.

## Next Steps

- Learn about [different backends](../guide/backends.md)
- Set up the [web interface](../guide/web-interface.md)
- Configure [password rotation](../guide/rotation.md)
'''
    
    write_file("docs/getting-started/quickstart.md", quickstart)
    print_success("Created docs/getting-started/quickstart.md")
    
    # Create basic examples
    print_info("Creating basic usage examples...")
    basic_examples = '''# Basic Usage Examples

Here are common ways to use dbcreds in your Python scripts.

## Simple Connection

```python
from dbcreds import get_connection

# Get a database connection
with get_connection("production") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    print(f"Total users: {count}")
```

## Using Connection Strings

```python
from dbcreds import get_connection_string
import psycopg2

# Get connection string
conn_string = get_connection_string("production")
print(f"Connection string: {conn_string}")

# Use with psycopg2 directly
conn = psycopg2.connect(conn_string)
```

## Error Handling

```python
from dbcreds import get_credentials
from dbcreds.core.exceptions import (
    CredentialNotFoundError, 
    PasswordExpiredError
)

try:
    creds = get_credentials("staging")
    print(f"Connecting to {creds.host}:{creds.port}")
except CredentialNotFoundError:
    print("Environment not found! Run: dbcreds add staging")
except PasswordExpiredError:
    print("Password expired! Run: dbcreds update staging --password")
```

## Getting Credential Details

```python
from dbcreds import get_credentials

# Get credentials object
creds = get_credentials("dev")

# Access individual components
print(f"Host: {creds.host}")
print(f"Port: {creds.port}")
print(f"Database: {creds.database}")
print(f"Username: {creds.username}")
print(f"Days until expiry: {creds.days_until_expiry()}")

# Get password (be careful with this!)
password = creds.password.get_secret_value()
```

## Multiple Environments

```python
from dbcreds import get_engine

# Define your environments
environments = ["dev", "staging", "prod"]

# Connect to each environment
for env in environments:
    try:
        engine = get_engine(env)
        with engine.connect() as conn:
            result = conn.execute("SELECT version()")
            version = result.scalar()
            print(f"{env}: {version}")
    except Exception as e:
        print(f"{env}: Failed - {e}")
```

## Environment-Based Configuration

```python
import os
from dbcreds import get_engine

# Use environment variable to determine which DB to connect to
env = os.getenv("APP_ENV", "dev")
engine = get_engine(env)

print(f"Connected to {env} database")
```
'''
    
    write_file("docs/examples/basic.md", basic_examples)
    print_success("Created docs/examples/basic.md")
    
    # Create security best practices
    print_info("Creating security best practices documentation...")
    security_docs = '''# Security Best Practices

This guide covers security best practices for using dbcreds in production environments.

## Credential Storage

### Use System Credential Stores

dbcreds automatically uses the most secure credential storage available:

- **Windows**: Windows Credential Manager
- **macOS**: Keychain
- **Linux**: Secret Service (libsecret)

Never store credentials in:
- Plain text files
- Environment variables (except for containers)
- Source code
- Version control

### Backend Priority

dbcreds tries backends in this order:
1. Platform-specific secure storage (Windows Credential Manager, Keychain)
2. Cross-platform keyring
3. Environment variables (for containers)
4. Configuration files (metadata only, no passwords)

## Web Interface Security

### Authentication

The web interface requires authentication. Change the default credentials immediately:

```python
# dbcreds/web/auth.py
DEFAULT_USERNAME = "admin"  # Change this
DEFAULT_PASSWORD_HASH = pwd_context.hash("your-secure-password")  # Change this
```

### HTTPS Only

Always use HTTPS in production:

```bash
# Use a reverse proxy like nginx
dbcreds-server --host 127.0.0.1 --port 8001

# nginx configuration
server {
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Security Headers

dbcreds automatically sets security headers:
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Strict-Transport-Security: max-age=31536000

## Password Management

### Regular Rotation

Set password expiry policies:

```python
# Set 30-day expiry
manager.set_credentials(
    "production",
    host="db.example.com",
    port=5432,
    database="myapp",
    username="appuser",
    password="secure-password",
    password_expires_days=30  # Expire in 30 days
)
```

### Strong Passwords

Use strong, unique passwords:
- Minimum 16 characters
- Mix of uppercase, lowercase, numbers, symbols
- No dictionary words
- No personal information

Generate secure passwords:

```python
import secrets
import string

def generate_password(length=24):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))
```

## Access Control

### Principle of Least Privilege

- Create separate database users for different applications
- Grant only necessary permissions
- Use read-only accounts where possible

### Environment Isolation

```python
# Separate credentials for each environment
manager.add_environment("dev", DatabaseType.POSTGRESQL)
manager.add_environment("staging", DatabaseType.POSTGRESQL)
manager.add_environment("prod", DatabaseType.POSTGRESQL, is_production=True)
```

## Network Security

### Use SSL/TLS

Always encrypt database connections:

```python
# PostgreSQL with SSL
creds.options["sslmode"] = "require"
creds.options["sslcert"] = "/path/to/client-cert.pem"
creds.options["sslkey"] = "/path/to/client-key.pem"

# MySQL with SSL
creds.options["ssl_ca"] = "/path/to/ca.pem"
creds.options["ssl_cert"] = "/path/to/client-cert.pem"
creds.options["ssl_key"] = "/path/to/client-key.pem"
```

### IP Whitelisting

Restrict database access by IP:
- Use firewall rules
- Configure database server access controls
- Use VPN for remote access
'''
    
    write_file("docs/security/best-practices.md", security_docs)
    print_success("Created docs/security/best-practices.md")

def create_examples():
    """Create usage example scripts."""
    print_header("💡 Creating Usage Examples")
    
    # Create examples directory
    Path("examples").mkdir(exist_ok=True)
    
    # Create ETL example
    print_info("Creating ETL example script...")
    etl_example = '''# etl_script.py
"""Example ETL script using dbcreds."""

import pandas as pd
from dbcreds import get_engine
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_sales_data(days_back=7):
    """Extract sales data from production database."""
    logger.info(f"Extracting sales data for last {days_back} days")
    
    engine = get_engine("production")
    
    query = """
        SELECT 
            order_id,
            customer_id,
            order_date,
            total_amount,
            status
        FROM orders
        WHERE order_date >= %(start_date)s
        AND status = 'completed'
    """
    
    start_date = datetime.now() - timedelta(days=days_back)
    
    df = pd.read_sql(
        query,
        engine,
        params={'start_date': start_date}
    )
    
    logger.info(f"Extracted {len(df)} orders")
    return df

def transform_sales_data(df):
    """Transform sales data for analytics."""
    logger.info("Transforming sales data")
    
    # Add calculated fields
    df['order_month'] = df['order_date'].dt.to_period('M')
    df['order_day_of_week'] = df['order_date'].dt.day_name()
    
    # Aggregate by customer
    customer_summary = df.groupby('customer_id').agg({
        'order_id': 'count',
        'total_amount': ['sum', 'mean'],
        'order_date': ['min', 'max']
    }).round(2)
    
    customer_summary.columns = [
        'order_count',
        'total_revenue',
        'avg_order_value',
        'first_order_date',
        'last_order_date'
    ]
    
    return customer_summary

def load_to_analytics(df):
    """Load transformed data to analytics database."""
    logger.info("Loading data to analytics database")
    
    engine = get_engine("analytics")
    
    df.to_sql(
        'customer_summary',
        engine,
        if_exists='replace',
        index=True,
        index_label='customer_id'
    )
    
    logger.info(f"Loaded {len(df)} customer records")

def main():
    """Run the ETL pipeline."""
    try:
        # Extract
        sales_df = extract_sales_data(days_back=30)
        
        # Transform
        customer_summary = transform_sales_data(sales_df)
        
        # Load
        load_to_analytics(customer_summary)
        
        logger.info("ETL pipeline completed successfully")
        
    except Exception as e:
        logger.error(f"ETL pipeline failed: {e}")
        raise

if __name__ == "__main__":
    main()
'''
    
    write_file("examples/etl_script.py", etl_example)
    print_success("Created examples/etl_script.py")
    
    # Create health check example
    print_info("Creating health check example script...")
    health_check = '''# db_health_check.py
"""Monitor database health across all environments."""

import time
from datetime import datetime
from dbcreds import CredentialManager, get_connection
import smtplib
from email.mime.text import MIMEText

def check_database_health(env_name):
    """Check if database is responsive."""
    start_time = time.time()
    
    try:
        with get_connection(env_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            
        response_time = (time.time() - start_time) * 1000  # ms
        return {
            'status': 'healthy',
            'response_time': round(response_time, 2),
            'error': None
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'response_time': None,
            'error': str(e)
        }

def check_all_environments():
    """Check health of all database environments."""
    manager = CredentialManager()
    results = {}
    
    for env in manager.list_environments():
        print(f"Checking {env.name}...")
        results[env.name] = check_database_health(env.name)
    
    return results

def send_alert(results):
    """Send email alert for unhealthy databases."""
    unhealthy = [
        f"{env}: {info['error']}"
        for env, info in results.items()
        if info['status'] == 'unhealthy'
    ]
    
    if not unhealthy:
        return
    
    # Configure your email settings
    msg = MIMEText(
        f"The following databases are unhealthy:\\n\\n" +
        "\\n".join(unhealthy)
    )
    msg['Subject'] = 'Database Health Alert'
    msg['From'] = 'monitoring@yourcompany.com'
    msg['To'] = 'ops@yourcompany.com'
    
    # Send email (configure SMTP server)
    # server = smtplib.SMTP('smtp.yourcompany.com')
    # server.send_message(msg)
    # server.quit()

def main():
    """Run health checks and report results."""
    print(f"Database Health Check - {datetime.now()}")
    print("-" * 50)
    
    results = check_all_environments()
    
    # Print results
    for env, info in results.items():
        if info['status'] == 'healthy':
            print(f"✓ {env}: {info['response_time']}ms")
        else:
            print(f"✗ {env}: {info['error']}")
    
    # Send alerts if needed
    send_alert(results)
    
    # Return exit code based on health
    unhealthy_count = sum(
        1 for info in results.values() 
        if info['status'] == 'unhealthy'
    )
    
    return unhealthy_count

if __name__ == "__main__":
    exit(main())
'''
    
    write_file("examples/db_health_check.py", health_check)
    print_success("Created examples/db_health_check.py")
    
    # Create multi-db query tool
    print_info("Creating multi-database query tool...")
    multi_db = '''# multi_db_query.py
"""Execute queries across multiple database environments."""

import argparse
import json
from tabulate import tabulate
from dbcreds import get_connection, CredentialManager

def execute_query(env_name, query):
    """Execute a query on a specific environment."""
    try:
        with get_connection(env_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            
            # Get column names
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            
            # Fetch results
            results = cursor.fetchall() if columns else []
            
            return {
                'success': True,
                'columns': columns,
                'rows': results,
                'error': None
            }
    except Exception as e:
        return {
            'success': False,
            'columns': [],
            'rows': [],
            'error': str(e)
        }

def main():
    parser = argparse.ArgumentParser(description='Execute queries across environments')
    parser.add_argument('query', help='SQL query to execute')
    parser.add_argument(
        '--envs', 
        nargs='+', 
        help='Environments to query (default: all)'
    )
    parser.add_argument(
        '--output', 
        choices=['table', 'json', 'csv'],
        default='table',
        help='Output format'
    )
    
    args = parser.parse_args()
    
    # Get environments
    manager = CredentialManager()
    if args.envs:
        environments = args.envs
    else:
        environments = [env.name for env in manager.list_environments()]
    
    # Execute query on each environment
    all_results = {}
    for env in environments:
        print(f"Querying {env}...")
        all_results[env] = execute_query(env, args.query)
    
    # Display results
    for env, result in all_results.items():
        print(f"\\n=== {env.upper()} ===")
        
        if result['success']:
            if result['rows']:
                if args.output == 'table':
                    print(tabulate(
                        result['rows'], 
                        headers=result['columns'],
                        tablefmt='grid'
                    ))
                elif args.output == 'json':
                    data = [
                        dict(zip(result['columns'], row))
                        for row in result['rows']
                    ]
                    print(json.dumps(data, indent=2, default=str))
                elif args.output == 'csv':
                    print(','.join(result['columns']))
                    for row in result['rows']:
                        print(','.join(str(v) for v in row))
            else:
                print("No results returned")
        else:
            print(f"ERROR: {result['error']}")

if __name__ == "__main__":
    main()
'''
    
    write_file("examples/multi_db_query.py", multi_db)
    print_success("Created examples/multi_db_query.py")

def create_additional_files():
    """Create additional configuration files."""
    print_header("📝 Creating Additional Files")
    
    # Create GitHub Actions workflow
    print_info("Creating GitHub Actions workflow...")
    Path(".github/workflows").mkdir(parents=True, exist_ok=True)
    
    workflow = '''name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12"]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install uv
        uv pip install -e ".[dev]"
    
    - name: Run tests
      run: |
        pytest
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true

  lint:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.11"
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install ruff black mypy
    
    - name: Run ruff
      run: ruff check .
    
    - name: Run black
      run: black --check .
    
    - name: Run mypy
      run: mypy dbcreds
'''
    
    write_file(".github/workflows/tests.yml", workflow)
    print_success("Created .github/workflows/tests.yml")
    
    # Create Makefile
    print_info("Creating Makefile...")
    makefile = '''# Makefile for dbcreds

.PHONY: help install test lint docs clean

help:
	@echo "Available commands:"
	@echo "  make install    Install package in development mode"
	@echo "  make test       Run tests"
	@echo "  make lint       Run linters"
	@echo "  make docs       Build documentation"
	@echo "  make serve-docs Serve documentation locally"
	@echo "  make clean      Clean build artifacts"

install:
	uv pip install -e ".[dev]"

test:
	pytest

test-cov:
	pytest --cov=dbcreds --cov-report=html --cov-report=term

lint:
	ruff check .
	black --check .
	mypy dbcreds

format:
	black .
	ruff check --fix .

docs:
	mkdocs build

serve-docs:
	mkdocs serve

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf site/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
'''
    
    write_file("Makefile", makefile)
    print_success("Created Makefile")
    
    # Create .gitignore if it doesn't exist
    if not Path(".gitignore").exists():
        print_info("Creating .gitignore...")
        gitignore = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/
htmlcov/

# Virtual environments
venv/
ENV/
env/
.venv

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# Documentation
site/
docs/_build/

# Database
*.db
*.sqlite
*.sqlite3

# Credentials
.env
.env.*
*.pem
*.key
*.crt

# OS
.DS_Store
Thumbs.db

# Project specific
~/.dbcreds/
backup_*/
'''
        
        write_file(".gitignore", gitignore)
        print_success("Created .gitignore")

def main():
    """Main function to run all setup tasks."""
    parser = argparse.ArgumentParser(description='Add features to dbcreds package')
    parser.add_argument('--skip-backup', action='store_true', help='Skip creating backup')
    parser.add_argument('--project-path', default='.', help='Path to project directory')
    
    args = parser.parse_args()
    
    # Change to project directory
    original_dir = os.getcwd()
    os.chdir(args.project_path)
    
    try:
        print(f"\n{Colors.BLUE}{Colors.BOLD}🚀 Adding security features, tests, and documentation to dbcreds{Colors.END}")
        print("=" * 60)
        
        # Create backup unless skipped
        if not args.skip_backup:
            create_backup('.')
        
        # Run all setup functions
        add_security_features()
        create_test_suite()
        create_documentation()
        create_examples()
        create_additional_files()
        
        # Success summary
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Successfully added features to dbcreds!{Colors.END}")
        print("=" * 60)
        
        print(f"\n{Colors.YELLOW}Next steps:{Colors.END}")
        print(f"{Colors.CYAN}1. Install development dependencies:{Colors.END}")
        print("   uv pip install -e '.[dev]'")
        print("")
        print(f"{Colors.CYAN}2. Run tests:{Colors.END}")
        print("   pytest")
        print("")
        print(f"{Colors.CYAN}3. Build documentation:{Colors.END}")
        print("   mkdocs serve")
        print("")
        print(f"{Colors.CYAN}4. Start web server:{Colors.END}")
        print("   dbcreds-server")
        print("")
        print(f"{Colors.CYAN}5. Run linting:{Colors.END}")
        print("   make lint")
        
        print(f"\n{Colors.RED}📝 Important Security Notes:{Colors.END}")
        print(f"{Colors.YELLOW}- Change default admin password in dbcreds/web/auth.py{Colors.END}")
        print(f"{Colors.YELLOW}- Use HTTPS in production for the web interface{Colors.END}")
        print(f"{Colors.YELLOW}- Review docs/security/best-practices.md{Colors.END}")
        
    except Exception as e:
        print_error(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    main()