#!/usr/bin/env python3
"""Generate missing documentation files for dbcreds."""

from pathlib import Path

# Define the documentation structure
DOCS = {
    "getting-started/installation.md": """# Installation

## Requirements

- Python 3.8+
- pip or uv

## Install from GitHub

```bash
pip install git+https://github.com/yourcompany/dbcreds.git
```

## Install with extras

```bash
# PostgreSQL only (default)
pip install git+https://github.com/yourcompany/dbcreds.git

# With MySQL support
pip install "git+https://github.com/yourcompany/dbcreds.git#egg=dbcreds[mysql]"

# With all databases
pip install "git+https://github.com/yourcompany/dbcreds.git#egg=dbcreds[mysql,oracle,mssql]"
```

## Development Installation

```bash
git clone https://github.com/yourcompany/dbcreds.git
cd dbcreds
uv venv
uv pip install -e ".[dev]"
```
""",
    "getting-started/configuration.md": """# Configuration

## Configuration Directory

dbcreds stores its configuration in `~/.dbcreds/` by default.

## Environment Variables

You can override the configuration directory:

```bash
export DBCREDS_CONFIG_DIR=/path/to/config
```

## Backend Configuration

dbcreds automatically detects available backends. See [Backends](../security/backends.md) for details.
""",
    "guide/cli.md": """# CLI Reference

The `dbcreds` command provides a rich CLI for managing credentials.

## Commands

::: dbcreds.cli
    options:
      show_source: false
      members: false

## Usage Examples

### Initialize
```bash
dbcreds init
```

### Add Environment
```bash
dbcreds add dev --type postgresql
```

### List Environments
```bash
dbcreds list
```

### Show Details
```bash
dbcreds show dev
```

### Test Connection
```bash
dbcreds test dev
```

### Check Expiry
```bash
dbcreds check
```
""",
    "guide/python-api.md": """# Python API

## Quick Start

```python
from dbcreds import get_connection, get_engine

# Get a connection
with get_connection("dev") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT 1")

# Get SQLAlchemy engine
engine = get_engine("dev")
```

## Shortcut Functions

::: dbcreds.utils.shortcuts
    options:
      show_source: true

## Core Classes

See [API Reference](../api/core.md) for detailed class documentation.
""",
    "guide/web-interface.md": """# Web Interface

## Starting the Server

```bash
dbcreds-server
```

Visit http://localhost:8000

## Features

- Visual credential management
- Password expiry tracking
- Team collaboration
- Secure authentication

## Configuration

The web interface uses FastAPI and HTMX for a modern, responsive UI.

## API Endpoints

::: dbcreds.web.main
    options:
      show_source: false
      members:
        - app
        - index
        - create_environment
        - list_environments
""",
    "guide/migration.md": """# Migration Guide

## From PowerShell Profile

If you have existing credentials in PowerShell, use the migration tool:

```bash
dbcreds-migrate --name dev
```

This will import credentials from:
- Environment variables (`DB_SERVER`, `DB_PORT`, etc.)
- Windows Credential Manager
- JSON config at `~/.db_credentials/config.json`

## Manual Migration

::: dbcreds.migrate
    options:
      show_source: false
""",
    "guide/backends.md": """# Storage Backends

dbcreds supports multiple credential storage backends.

## Available Backends

### Keyring Backend
Cross-platform using system credential stores.

### Windows Credential Manager
Native Windows credential storage.

### Environment Variables
Read credentials from environment.

### Config File
JSON file storage (metadata only).

## Backend Priority

Backends are tried in order of security and availability.

See [Backend API](../api/backends.md) for implementation details.
""",
    "guide/rotation.md": """# Password Rotation

## Automatic Expiry Tracking

dbcreds tracks password age and expiry:

```python
from dbcreds import get_credentials

creds = get_credentials("dev")
days_left = creds.days_until_expiry()
if creds.is_password_expired():
    print("Password expired!")
```

## Setting Expiry

```bash
# Set 90-day expiry
dbcreds add dev --expires-days 90

# Update expiry
dbcreds update dev --expires-days 180
```

## Checking Status

```bash
# Check all environments
dbcreds check
```
""",
    "examples/sqlalchemy.md": """# SQLAlchemy Examples

## Basic Usage

```python
from dbcreds import get_engine
import pandas as pd

# Get engine for environment
engine = get_engine("dev")

# Use with pandas
df = pd.read_sql("SELECT * FROM users LIMIT 10", engine)

# Use with SQLAlchemy ORM
from sqlalchemy.orm import Session

with Session(engine) as session:
    result = session.execute("SELECT 1")
```

## Async Support

```python
from dbcreds import get_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

engine = await get_async_engine("dev")

async with AsyncSession(engine) as session:
    result = await session.execute("SELECT 1")
```
""",
    "examples/pandas.md": """# Pandas Examples

## Reading Data

```python
import pandas as pd
from dbcreds import get_connection, get_engine

# Using connection
with get_connection("dev") as conn:
    df = pd.read_sql("SELECT * FROM sales", conn)

# Using engine (recommended)
engine = get_engine("dev")
df = pd.read_sql_table("sales", engine)
```

## Writing Data

```python
# Write DataFrame to database
df.to_sql("sales_backup", engine, if_exists="replace", index=False)
```

## Large Datasets

```python
# Read in chunks
for chunk in pd.read_sql("SELECT * FROM large_table", 
                         engine, chunksize=10000):
    process(chunk)
```
""",
    "examples/async.md": """# Async Examples

## AsyncIO Support

```python
import asyncio
from dbcreds import get_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

async def fetch_data():
    engine = await get_async_engine("dev")
    
    async with AsyncSession(engine) as session:
        result = await session.execute("SELECT * FROM users")
        return result.fetchall()

# Run async function
data = asyncio.run(fetch_data())
```

## Async Context Manager

```python
async def process_data():
    engine = await get_async_engine("dev")
    
    async with engine.connect() as conn:
        result = await conn.execute("SELECT COUNT(*) FROM orders")
        count = result.scalar()
        return count
```
""",
    "security/backends.md": """# Security Backends

## Backend Security

Each backend provides different security guarantees:

### Keyring Backend
- Uses OS-native credential storage
- Encrypted at rest
- User-level isolation

### Windows Credential Manager
- Windows DPAPI encryption
- Integrated with Windows security

### Environment Variables
- No encryption
- Suitable for containers
- Should use secrets management

## Backend Interface

See the [Backend API Reference](../api/backends.md) for implementation details.
""",
    "api/core.md": """# Core API

## CredentialManager

::: dbcreds.core.manager.CredentialManager
    options:
      show_source: false

## Models

::: dbcreds.core.models.DatabaseCredentials
    options:
      show_source: false

::: dbcreds.core.models.Environment
    options:
      show_source: false

::: dbcreds.core.models.DatabaseType
    options:
      show_source: false

## Exceptions

::: dbcreds.core.exceptions
    options:
      show_source: false
""",
    "api/backends.md": """# Backends API

## Base Backend

::: dbcreds.backends.base.CredentialBackend
    options:
      show_source: true

## Keyring Backend

::: dbcreds.backends.keyring.KeyringBackend
    options:
      show_source: false

## Windows Backend

::: dbcreds.backends.windows.WindowsCredentialBackend
    options:
      show_source: false

## Environment Backend

::: dbcreds.backends.environment.EnvironmentBackend
    options:
      show_source: false

## Config Backend

::: dbcreds.backends.config.ConfigFileBackend
    options:
      show_source: false
""",
    "api/cli.md": """# CLI API

## Main CLI Application

::: dbcreds.cli.app
    options:
      show_source: false

## Commands

::: dbcreds.cli.init
    options:
      show_source: false

::: dbcreds.cli.add
    options:
      show_source: false

::: dbcreds.cli.list
    options:
      show_source: false

::: dbcreds.cli.show
    options:
      show_source: false

::: dbcreds.cli.test
    options:
      show_source: false

::: dbcreds.cli.remove
    options:
      show_source: false

::: dbcreds.cli.update
    options:
      show_source: false

::: dbcreds.cli.check
    options:
      show_source: false

::: dbcreds.cli.export
    options:
      show_source: false
""",
    "api/web.md": """# Web API

## FastAPI Application

::: dbcreds.web.main.app
    options:
      show_source: false

## Routes

::: dbcreds.web.main
    options:
      show_source: false
      members:
        - index
        - create_environment
        - list_environments
        - edit_environment_form
        - update_environment
        - test_environment
        - get_environment_expiry

## Authentication

::: dbcreds.web.auth
    options:
      show_source: false
      members:
        - get_current_user
        - authenticate_user

## Error Handling

::: dbcreds.web.errors.WebErrorHandler
    options:
      show_source: false
""",
}


def main():
    """Create missing documentation files."""
    import sys

    # Check for --force flag
    force = "--force" in sys.argv

    docs_dir = Path("docs")

    if not docs_dir.exists():
        print("Error: docs directory not found. Run this from the project root.")
        return

    created = 0
    skipped = 0
    updated = 0

    for filepath, content in DOCS.items():
        full_path = docs_dir / filepath

        # Check if file exists
        if full_path.exists():
            if force:
                full_path.write_text(content)
                print(f"Updated {filepath}")
                updated += 1
            else:
                print(f"Skipping {filepath} - already exists")
                skipped += 1
            continue

        # Create parent directories
        full_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the file
        full_path.write_text(content)
        print(f"Created {filepath}")
        created += 1

    print(
        f"\nSummary: Created {created} files, updated {updated} files, skipped {skipped} existing files"
    )
    if skipped > 0 and not force:
        print("\nTip: Use --force to overwrite existing files")
    print("\nNow run 'mkdocs serve' to view the documentation")


if __name__ == "__main__":
    main()
