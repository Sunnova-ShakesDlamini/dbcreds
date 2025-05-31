# README.md
# dbcreds

Professional database credentials management with security and team collaboration in mind.

## Features

- 🔐 **Secure Storage**: Multiple backend support (Windows Credential Manager, macOS Keychain, Linux Secret Service)
- 🌍 **Multi-Environment**: Manage credentials for development, staging, and production
- 🚀 **Rich CLI**: Beautiful command-line interface with Rich and Typer
- 🌐 **Web UI**: Optional FastAPI web interface with HTMX
- 📊 **Multi-Database**: Support for PostgreSQL, MySQL, Oracle, SQL Server
- 🔄 **Password Rotation**: Track password age and expiration
- 📝 **Full Documentation**: Comprehensive docs with mkdocstrings
- 🎯 **Type Safety**: Pydantic models for validation

## Installation

Install directly from GitHub using pip:

```bash
pip install git+https://github.com/yourcompany/dbcreds.git
```

Or using uv:

```bash
uv pip install git+https://github.com/yourcompany/dbcreds.git
```

For development with additional database support:

```bash
# PostgreSQL only (default)
pip install git+https://github.com/yourcompany/dbcreds.git

# With MySQL support
pip install "git+https://github.com/yourcompany/dbcreds.git#egg=dbcreds[mysql]"

# With all databases
pip install "git+https://github.com/yourcompany/dbcreds.git#egg=dbcreds[mysql,oracle,mssql]"
```

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

```python
from dbcreds import get_engine, get_connection

# Get SQLAlchemy engine
engine = get_engine("dev")

# Get connection
with get_connection("prod") as conn:
    df = pd.read_sql("SELECT * FROM users LIMIT 10", conn)

# Async support
from dbcreds import get_async_engine

async_engine = await get_async_engine("dev")
```

## CLI Usage

```bash
# List all environments
dbcreds list

# Show specific environment (without password)
dbcreds show dev

# Test connection
dbcreds test dev

# Update password
dbcreds update dev --password

# Remove environment
dbcreds remove dev

# Check password expiry
dbcreds check

# Export connection string
dbcreds export dev --format uri
```

## Web Interface

Start the web interface for team credential management:

```bash
dbcreds-server
# Visit http://localhost:8000
```

## Configuration

dbcreds stores configuration in `~/.dbcreds/config.json` and credentials in your system's secure storage.

## Development

```bash
# Clone the repository
git clone https://github.com/yourcompany/dbcreds.git
cd dbcreds

# Create virtual environment with uv
uv venv
uv pip install -e ".[dev]"

# Run tests
pytest

# Build documentation
mkdocs serve
```

## Security

- Credentials are never stored in plain text
- Each environment has isolated credentials
- Password rotation reminders
- Audit logging for credential access
- Team-based access control in web UI

## License

MIT License - see LICENSE file for details.