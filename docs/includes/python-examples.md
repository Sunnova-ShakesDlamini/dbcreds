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