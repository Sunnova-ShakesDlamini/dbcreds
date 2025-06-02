```python
# Quick connection
from dbcreds import get_connection_string
conn = get_connection_string("prod")

# With SQLAlchemy
from dbcreds import get_engine
engine = get_engine("prod")

# With pandas
import pandas as pd
df = pd.read_sql("SELECT * FROM users", get_connection_string("prod"))

# Async support
from dbcreds import get_async_engine
async_engine = await get_async_engine("prod")
```
