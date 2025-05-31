# SQLAlchemy Examples

## Basic Usage

```python
from dbcreds import get_engine
import pandas as pd

# Get engine for environment
engine = get_engine("dev")

# Use with pandas
df = pd.read_sql("SELECT * FROM users LIMIT 10", engine)

# Use with SQLAlchemy ORM
from sqlalchemy.orm import Session

with Session(engine) as session:
    result = session.execute("SELECT 1")
```

## Async Support

```python
from dbcreds import get_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

engine = await get_async_engine("dev")

async with AsyncSession(engine) as session:
    result = await session.execute("SELECT 1")
```
