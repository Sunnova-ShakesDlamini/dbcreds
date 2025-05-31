# Pandas Examples

## Reading Data

```python
import pandas as pd
from dbcreds import get_connection, get_engine

# Using connection
with get_connection("dev") as conn:
    df = pd.read_sql("SELECT * FROM sales", conn)

# Using engine (recommended)
engine = get_engine("dev")
df = pd.read_sql_table("sales", engine)
```

## Writing Data

```python
# Write DataFrame to database
df.to_sql("sales_backup", engine, if_exists="replace", index=False)
```

## Large Datasets

```python
# Read in chunks
for chunk in pd.read_sql("SELECT * FROM large_table", 
                         engine, chunksize=10000):
    process(chunk)
```
