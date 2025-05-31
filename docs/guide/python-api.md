# Python API

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
