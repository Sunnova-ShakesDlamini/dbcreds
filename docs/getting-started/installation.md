# Installation

## Requirements

- Python 3.8+
- pip or uv

## Install from GitHub

```bash
pip install git+https://github.com/Sunnova-ShakesDlamini/dbcreds
```

## Install with extras

```bash
# PostgreSQL only (default)
pip install git+https://github.com/Sunnova-ShakesDlamini/dbcreds

# With MySQL support
pip install "git+https://github.com/Sunnova-ShakesDlamini/dbcreds#egg=dbcreds[mysql]"

# With all databases
pip install "git+https://github.com/Sunnova-ShakesDlamini/dbcreds#egg=dbcreds[mysql,oracle,mssql]"
```

## Development Installation

```bash
git clone https://github.com/Sunnova-ShakesDlamini/dbcreds
cd dbcreds
uv venv
uv pip install -e ".[dev]"
```
