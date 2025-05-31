#!/usr/bin/env python3
"""Create all the snippet files for dbcreds documentation."""

from pathlib import Path

# Define all snippets
SNIPPETS = {
    "installation-basic.md": """```bash
pip install git+https://github.com/Sunnova-ShakesDlamini/dbcreds.git
```""",
    "installation-full.md": """Install directly from GitHub using pip:

```bash
pip install git+https://github.com/Sunnova-ShakesDlamini/dbcreds.git
```

Or using uv:

```bash
uv pip install git+https://github.com/Sunnova-ShakesDlamini/dbcreds.git
```

For development with additional database support:

```bash
# PostgreSQL only (default)
pip install git+https://github.com/Sunnova-ShakesDlamini/dbcreds.git

# With MySQL support
pip install "git+https://github.com/Sunnova-ShakesDlamini/dbcreds.git#egg=dbcreds[mysql]"

# With all databases
pip install "git+https://github.com/Sunnova-ShakesDlamini/dbcreds.git#egg=dbcreds[mysql,oracle,mssql]"
```""",
    "quickstart.md": """```bash
# Install dbcreds
pip install git+https://github.com/Sunnova-ShakesDlamini/dbcreds.git

# Initialize and add your first environment
dbcreds init
dbcreds add dev --type postgresql

# Use in your Python code
from dbcreds import get_engine
engine = get_engine("dev")
```""",
    "features-list.md": """- 🔐 **Secure Storage**: Multiple backend support (Windows Credential Manager, macOS Keychain, Linux Secret Service)
- 🌍 **Multi-Environment**: Manage credentials for development, staging, and production
- 🚀 **Rich CLI**: Beautiful command-line interface with Rich and Typer
- 🌐 **Web UI**: Optional FastAPI web interface with HTMX
- 📊 **Multi-Database**: Support for PostgreSQL, MySQL, Oracle, SQL Server
- 🔄 **Password Rotation**: Track password age and expiration
- 📝 **Full Documentation**: Comprehensive docs with mkdocstrings
- 🎯 **Type Safety**: Pydantic models for validation""",
    "installation-tabs.md": """=== "pip"
    ```bash
    pip install git+https://github.com/Sunnova-ShakesDlamini/dbcreds.git
    ```

=== "uv"
    ```bash
    uv pip install git+https://github.com/Sunnova-ShakesDlamini/dbcreds.git
    ```

=== "Development"
    ```bash
    git clone https://github.com/Sunnova-ShakesDlamini/dbcreds.git
    cd dbcreds
    uv venv
    uv pip install -e ".[dev]"
    ```""",
    "cli-examples.md": """```bash
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
```""",
    "python-examples.md": """```python
from dbcreds import get_engine, get_connection

# Get SQLAlchemy engine
engine = get_engine("dev")

# Get connection
with get_connection("prod") as conn:
    df = pd.read_sql("SELECT * FROM users LIMIT 10", conn)

# Async support
from dbcreds import get_async_engine

async_engine = await get_async_engine("dev")
```""",
    "development.md": """```bash
# Clone the repository
git clone https://github.com/Sunnova-ShakesDlamini/dbcreds.git
cd dbcreds

# Create virtual environment with uv
uv venv
uv pip install -e ".[dev]"

# Run tests
pytest

# Build documentation
mkdocs serve
```""",
    "key-features.md": """## 🎯 Key Features

- **Multi-Environment**: Manage dev, staging, and production credentials
- **Secure Storage**: Uses your OS's native credential manager
- **Password Rotation**: Built-in expiry tracking and notifications
- **Rich CLI**: Beautiful terminal interface with auto-completion
- **Type Safety**: Full type hints with Pydantic validation
- **Multi-Database**: PostgreSQL, MySQL, Oracle, SQL Server support
- **Team Ready**: Web UI for secure credential sharing
- **Easy Integration**: Works with SQLAlchemy, pandas, and more""",
}


def create_snippets():
    """Create all snippet files."""
    # Create includes directory
    includes_dir = Path("docs/includes")
    includes_dir.mkdir(parents=True, exist_ok=True)

    # Create each snippet file
    for filename, content in SNIPPETS.items():
        filepath = includes_dir / filename
        filepath.write_text(content, encoding="utf-8")
        print(f"✅ Created {filepath}")

    print(f"\n🎉 Created {len(SNIPPETS)} snippet files in {includes_dir}")
    print("\nNow you can use these snippets in your documentation:")
    print('  In README.md:     --8<-- "docs/includes/snippet-name.md"')
    print('  In docs/*.md:     --8<-- "includes/snippet-name.md"')


def show_example_usage():
    """Show example of how to use snippets in README and docs."""

    readme_example = """# Example README.md using snippets

# dbcreds

Professional database credentials management with security and team collaboration in mind.

## Features

--8<-- "docs/includes/features-list.md"

## Installation

--8<-- "docs/includes/installation-full.md"

## Quick Start

--8<-- "docs/includes/quickstart.md"

## CLI Usage

--8<-- "docs/includes/cli-examples.md"

## Python API

--8<-- "docs/includes/python-examples.md"
"""

    homepage_example = """# Example docs/index.md using snippets (with beautiful styling preserved)

# Welcome to dbcreds

<div class="hero-gradient">
  <!-- Your beautiful hero section -->
</div>

## 🔐 Secure by Design

<div class="grid" style="...">
  <!-- Your beautiful feature cards -->
</div>

## ⚡ Quick Start

--8<-- "includes/quickstart.md"

## 🔧 Installation

--8<-- "includes/installation-tabs.md"

<!-- Rest of your beautiful homepage -->
"""

    print("\n" + "=" * 60)
    print("EXAMPLE: README.md")
    print("=" * 60)
    print(readme_example)

    print("\n" + "=" * 60)
    print("EXAMPLE: docs/index.md")
    print("=" * 60)
    print(homepage_example)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Create snippet files for dbcreds docs"
    )
    parser.add_argument(
        "--show-examples",
        action="store_true",
        help="Show example usage in README and docs",
    )

    args = parser.parse_args()

    create_snippets()

    if args.show_examples:
        show_example_usage()
