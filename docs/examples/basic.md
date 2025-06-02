# Basic Usage Examples

This guide covers the most common dbcreds usage patterns.

## 🚀 Quick Connection

The simplest way to get a database connection:

```python
from dbcreds import get_connection_string

# Get connection string
conn_string = get_connection_string("prod")
print(conn_string)
# postgresql://user:pass@localhost:5432/mydb
```

## 📊 With Pandas

```python
import pandas as pd
from dbcreds import get_connection_string

# Read data directly
df = pd.read_sql(
    "SELECT * FROM users LIMIT 10",
    get_connection_string("analytics")
)

# Write data
df.to_sql(
    "user_backup",
    get_connection_string("backup"),
    if_exists="replace",
    index=False
)
```

## 🔧 With SQLAlchemy

```python
from sqlalchemy import create_engine, text
from dbcreds import get_engine

# Get pre-configured engine
engine = get_engine("prod")

# Execute queries
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM users"))
    count = result.scalar()
    print(f"Total users: {count}")

# Or use ORM
from sqlalchemy.orm import Session

with Session(engine) as session:
    # Your ORM queries here
    pass
```

## 🐘 With psycopg2

```python
from dbcreds import get_connection

# Using context manager
with get_connection("prod") as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT version()")
        version = cur.fetchone()[0]
        print(f"PostgreSQL version: {version}")
```

## 🔑 Managing Credentials

```python
from dbcreds import CredentialManager, DatabaseType

# Initialize manager
manager = CredentialManager()

# Add new environment
manager.add_environment(
    "staging",
    DatabaseType.POSTGRESQL,
    description="Staging database",
    is_production=False
)

# Set credentials
manager.set_credentials(
    "staging",
    host="staging.db.company.com",
    port=5432,
    database="app_staging",
    username="staging_user",
    password="secure_password",
    password_expires_days=90
)

# List all environments
for env in manager.list_environments():
    print(f"{env.name}: {env.database_type.value}")
```

## ⚡ Fast Mode Examples

### Environment Variables

```bash
# Set credentials via environment
export DBCREDS_PROD_HOST=db.company.com
export DBCREDS_PROD_PORT=5432
export DBCREDS_PROD_DATABASE=production
export DBCREDS_PROD_USERNAME=app_user
export DBCREDS_PROD_PASSWORD=secure_pass

# Now Python can access instantly
python -c "from dbcreds import get_connection_string; print(get_connection_string('prod'))"
```

### Direct Fast Access

```python
# Skip all initialization
from dbcreds.fast import get_connection_string

# Ultra-fast connection string
conn = get_connection_string("prod")
```

## 🔒 Security Examples

### Password-Free Connection Strings

```python
from dbcreds import get_connection_string

# Get connection string without password
safe_uri = get_connection_string("prod", include_password=False)
print(safe_uri)
# postgresql://user@localhost:5432/mydb

# Useful for logging or display
print(f"Connecting to: {safe_uri}")
```

### Checking Password Expiry

```python
from dbcreds import get_credentials

# Get full credentials
creds = get_credentials("prod")

# Check expiry
if creds.is_password_expired():
    print("WARNING: Password has expired!")
else:
    days_left = creds.days_until_expiry()
    if days_left and days_left < 14:
        print(f"Password expires in {days_left} days")
```

## 🔄 Connection Pooling

```python
from sqlalchemy.pool import QueuePool
from dbcreds import get_engine

# Create engine with custom pool settings
engine = get_engine(
    "prod",
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600,   # Recycle connections after 1 hour
)

# Use for multiple queries
with engine.connect() as conn:
    # Multiple queries share the pool
    users = conn.execute("SELECT * FROM users").fetchall()
    orders = conn.execute("SELECT * FROM orders").fetchall()
```

## 📝 Error Handling

```python
from dbcreds import get_connection_string, CredentialNotFoundError

try:
    conn_string = get_connection_string("nonexistent")
except ValueError as e:  # Fast mode error
    print(f"Credentials not found: {e}")
    
# Or with full manager
from dbcreds import CredentialManager

manager = CredentialManager()
try:
    creds = manager.get_credentials("nonexistent")
except CredentialNotFoundError as e:
    print(f"Environment not configured: {e}")
```

## 🎯 Environment-Specific Code

```python
import os
from dbcreds import get_connection_string

# Determine environment
env = os.getenv("APP_ENV", "dev")

# Get appropriate connection
conn_string = get_connection_string(env)

# Environment-specific settings
if env == "prod":
    engine_kwargs = {
        "pool_size": 20,
        "max_overflow": 30,
        "echo": False
    }
else:
    engine_kwargs = {
        "pool_size": 5,
        "max_overflow": 10,
        "echo": True  # SQL logging in dev
    }

from sqlalchemy import create_engine
engine = create_engine(conn_string, **engine_kwargs)
```

## 🚀 Next Steps

- Learn about [SQLAlchemy integration](sqlalchemy.md)
- Explore [async support](async.md)
- Use with [Pandas](pandas.md)
- Build [dashboards with marimo](marimo.md)
