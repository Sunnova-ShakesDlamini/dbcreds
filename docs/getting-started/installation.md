# Installation

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
