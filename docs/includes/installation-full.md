Install directly from GitHub using pip:

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
```