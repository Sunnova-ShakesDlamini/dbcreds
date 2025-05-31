# Async Examples

## AsyncIO Support

```python
import asyncio
from dbcreds import get_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

async def fetch_data():
    engine = await get_async_engine("dev")
    
    async with AsyncSession(engine) as session:
        result = await session.execute("SELECT * FROM users")
        return result.fetchall()

# Run async function
data = asyncio.run(fetch_data())
```

## Async Context Manager

```python
async def process_data():
    engine = await get_async_engine("dev")
    
    async with engine.connect() as conn:
        result = await conn.execute("SELECT COUNT(*) FROM orders")
        count = result.scalar()
        return count
```
