# add-dbcreds-features-fixed.ps1
# PowerShell script to add security features, tests, documentation, and examples to dbcreds

param(
    [Parameter(Mandatory=$false)]
    [string]$ProjectPath = ".",
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipBackup = $false
)

# Set strict mode
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Helper functions
function Write-Success($message) { Write-Host "✓ $message" -ForegroundColor Green }
function Write-Info($message) { Write-Host "ℹ $message" -ForegroundColor Cyan }
function Write-Warning($message) { Write-Host "⚠ $message" -ForegroundColor Yellow }
function Write-Error($message) { Write-Host "✗ $message" -ForegroundColor Red }

# Function to write file content safely
function Write-FileContent {
    param(
        [string]$Path,
        [string]$Content
    )
    
    $directory = Split-Path -Parent $Path
    if ($directory -and !(Test-Path $directory)) {
        New-Item -ItemType Directory -Force -Path $directory | Out-Null
    }
    
    [System.IO.File]::WriteAllText($Path, $Content, [System.Text.Encoding]::UTF8)
}

# Change to project directory
Push-Location $ProjectPath

try {
    Write-Host "`n🚀 Adding security features, tests, and documentation to dbcreds" -ForegroundColor Blue
    Write-Host "=" * 60 -ForegroundColor Blue

    # Create backup if not skipped
    if (-not $SkipBackup) {
        Write-Info "Creating backup of current project..."
        $backupDir = "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        Copy-Item -Path "." -Destination $backupDir -Recurse -Exclude @(".git", "__pycache__", "*.pyc", ".pytest_cache", "backup_*")
        Write-Success "Backup created: $backupDir"
    }

    # 1. Add Security Features
    Write-Host "`n📔 Adding Security Features" -ForegroundColor Yellow
    Write-Host "-" * 40

    # Create auth.py for web interface
    Write-Info "Creating web authentication module..."
    $authContent = '# dbcreds/web/auth.py
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
    return credentials.username'
    
    Write-FileContent -Path "dbcreds/web/auth.py" -Content $authContent
    Write-Success "Created dbcreds/web/auth.py"

    # Create security.py for core
    Write-Info "Creating core security module..."
    $securityContent = '# dbcreds/core/security.py
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
    
    return masked'
    
    Write-FileContent -Path "dbcreds/core/security.py" -Content $securityContent
    Write-Success "Created dbcreds/core/security.py"

    # 2. Create Test Structure
    Write-Host "`n🧪 Creating Test Suite" -ForegroundColor Yellow
    Write-Host "-" * 40

    # Create test directories
    $testDirs = @(
        "tests",
        "tests/test_core",
        "tests/test_backends", 
        "tests/test_cli",
        "tests/test_web"
    )

    foreach ($dir in $testDirs) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
        New-Item -ItemType File -Force -Path "$dir/__init__.py" | Out-Null
    }
    Write-Success "Created test directory structure"

    # Create conftest.py
    Write-Info "Creating test fixtures..."
    $conftestContent = '# tests/conftest.py
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
    }'
    
    Write-FileContent -Path "tests/conftest.py" -Content $conftestContent
    Write-Success "Created tests/conftest.py"

    # Create test_manager.py
    Write-Info "Creating manager tests..."
    $testManagerContent = '# tests/test_core/test_manager.py
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
        assert "prod" in env_names'
    
    Write-FileContent -Path "tests/test_core/test_manager.py" -Content $testManagerContent
    Write-Success "Created tests/test_core/test_manager.py"

    # Create test_models.py
    Write-Info "Creating model tests..."
    $testModelsContent = '# tests/test_core/test_models.py
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
        assert "user" in conn_str_no_pwd'
    
    Write-FileContent -Path "tests/test_core/test_models.py" -Content $testModelsContent
    Write-Success "Created tests/test_core/test_models.py"

    # 3. Create Documentation Structure
    Write-Host "`n📚 Creating Documentation" -ForegroundColor Yellow
    Write-Host "-" * 40

    # Create docs directories
    $docDirs = @(
        "docs",
        "docs/getting-started",
        "docs/guide",
        "docs/examples",
        "docs/security",
        "docs/api"
    )

    foreach ($dir in $docDirs) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
    Write-Success "Created documentation directory structure"

    # Create mkdocs.yml
    Write-Info "Creating MkDocs configuration..."
    $mkdocsContent = '# mkdocs.yml
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
      link: https://twitter.com/yourcompany'
    
    Write-FileContent -Path "mkdocs.yml" -Content $mkdocsContent
    Write-Success "Created mkdocs.yml"

    # 4. Create Usage Examples
    Write-Host "`n💡 Creating Usage Examples" -ForegroundColor Yellow
    Write-Host "-" * 40

    # Create examples directory
    New-Item -ItemType Directory -Force -Path "examples" | Out-Null

    # Create ETL example script
    Write-Info "Creating ETL example script..."
    $etlExample = @"
# etl_script.py
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
"@
    Write-FileContent -Path "examples/etl_script.py" -Content $etlExample
    Write-Success "Created examples/etl_script.py"

    # Create health check script
    Write-Info "Creating health check example script..."
    $healthCheckExample = @"
# db_health_check.py
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
        f"The following databases are unhealthy:\n\n" +
        "\n".join(unhealthy)
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
"@
    Write-FileContent -Path "examples/db_health_check.py" -Content $healthCheckExample
    Write-Success "Created examples/db_health_check.py"

    # 5. Create pytest.ini
    Write-Info "Creating pytest configuration..."
    $pytestIni = @"
[tool:pytest]
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
"@
    Write-FileContent -Path "pytest.ini" -Content $pytestIni
    Write-Success "Created pytest.ini"

    # 6. Create GitHub Actions workflow
    Write-Info "Creating GitHub Actions workflow..."
    New-Item -ItemType Directory -Force -Path ".github/workflows" | Out-Null
    $workflowContent = @"
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: `${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12"]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python `${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: `${{ matrix.python-version }}
    
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
"@
    Write-FileContent -Path ".github/workflows/tests.yml" -Content $workflowContent
    Write-Success "Created .github/workflows/tests.yml"

    # 7. Create Makefile
    Write-Info "Creating Makefile..."
    $makefile = @"
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
"@
    Write-FileContent -Path "Makefile" -Content $makefile
    Write-Success "Created Makefile"

    # Create basic documentation files
    Write-Info "Creating documentation files..."
    
    # Create docs/index.md
    $docsIndex = @"
# dbcreds

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

## Getting Started

Check out the [Quick Start Guide](getting-started/quickstart.md) to get up and running in minutes!
"@
    Write-FileContent -Path "docs/index.md" -Content $docsIndex
    Write-Success "Created docs/index.md"

    # Create docs/getting-started/quickstart.md
    $quickstart = @"
# Quick Start Guide

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

## Check Password Expiry

```bash
dbcreds check
```

This shows you which passwords are expired or expiring soon.
"@
    Write-FileContent -Path "docs/getting-started/quickstart.md" -Content $quickstart
    Write-Success "Created docs/getting-started/quickstart.md"

    # Summary
    Write-Host "`n✅ Successfully added features to dbcreds!" -ForegroundColor Green
    Write-Host "=" * 60 -ForegroundColor Green
    
    Write-Host "`nNext steps:" -ForegroundColor Yellow
    Write-Host "1. Install development dependencies:" -ForegroundColor Cyan
    Write-Host "   uv pip install -e '.[dev]'" -ForegroundColor White
    Write-Host ""
    Write-Host "2. Run tests:" -ForegroundColor Cyan
    Write-Host "   pytest" -ForegroundColor White
    Write-Host ""
    Write-Host "3. Build documentation:" -ForegroundColor Cyan
    Write-Host "   mkdocs serve" -ForegroundColor White
    Write-Host ""
    Write-Host "4. Start web server:" -ForegroundColor Cyan
    Write-Host "   dbcreds-server" -ForegroundColor White
    Write-Host ""
    Write-Host "5. Run linting:" -ForegroundColor Cyan
    Write-Host "   make lint" -ForegroundColor White

    Write-Host "`n📝 Important Security Notes:" -ForegroundColor Red
    Write-Host "- Change default admin password in dbcreds/web/auth.py" -ForegroundColor Yellow
    Write-Host "- Use HTTPS in production for the web interface" -ForegroundColor Yellow
    Write-Host "- Review docs/security/best-practices.md" -ForegroundColor Yellow
    
} catch {
    Write-Error "An error occurred: $_"
    exit 1
} finally {
    Pop-Location
}