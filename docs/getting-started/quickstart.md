# Quick Start Guide

Get started with dbcreds in just a few minutes!

## Installation

```bash
pip install git+https://github.com/Sunnova-ShakesDlamini/dbcreds
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
