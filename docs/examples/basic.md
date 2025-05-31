# Basic Usage Examples

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
