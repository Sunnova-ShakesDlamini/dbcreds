# Using dbcreds with Marimo Notebooks

dbcreds v2.0+ has built-in support for [marimo](https://marimo.io/) notebooks with automatic fast mode detection.

## 🚀 Quick Start

No configuration needed - just import and use:

```python
# In a marimo notebook
import marimo as mo
from dbcreds import get_connection_string
import pandas as pd
import sqlalchemy as sa

# Get connection string - lightning fast!
conn_string = get_connection_string("prod")

# Create engine and query data
engine = sa.create_engine(conn_string)
df = pd.read_sql("SELECT * FROM users LIMIT 10", engine)

# Display in marimo
mo.md(f"Found {len(df)} users")
```

## 📊 Data Analysis Example

```python
import marimo as mo
import pandas as pd
import plotly.express as px
from dbcreds import get_connection_string

# Get connection - no hanging!
conn = get_connection_string("analytics")

# Load data
query = """
SELECT 
    DATE_TRUNC('day', created_at) as date,
    COUNT(*) as signups
FROM users
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY 1
ORDER BY 1
"""

df = pd.read_sql(query, conn)

# Visualize
fig = px.line(df, x='date', y='signups', 
              title='Daily Signups - Last 30 Days')

mo.ui.plotly(fig)
```

## 🔄 Interactive Queries

```python
import marimo as mo
from dbcreds import get_connection_string
import pandas as pd

# Create UI elements
table_name = mo.ui.text(value="users", label="Table Name")
limit = mo.ui.slider(1, 100, value=10, label="Limit")

mo.md(f"""
## Interactive Database Explorer

Table: {table_name}  
Limit: {limit}
""")

# When values change, this runs automatically
if table_name.value:
    conn = get_connection_string("prod")
    query = f"SELECT * FROM {table_name.value} LIMIT {limit.value}"
    
    try:
        df = pd.read_sql(query, conn)
        mo.ui.dataframe(df)
    except Exception as e:
        mo.md(f"❌ Error: {e}")
```

## 🎨 Dashboard Example

```python
import marimo as mo
import pandas as pd
import altair as alt
from dbcreds import get_connection_string
from datetime import datetime, timedelta

# Get connection
conn = get_connection_string("analytics")

# Date range picker
date_range = mo.ui.date_range(
    start=datetime.now() - timedelta(days=30),
    stop=datetime.now(),
    label="Date Range"
)

# Metric selector
metric = mo.ui.dropdown(
    options=["Revenue", "Users", "Orders"],
    value="Revenue",
    label="Metric"
)

mo.md(f"""
# 📊 Business Dashboard

**Date Range:** {date_range.value[0].strftime('%Y-%m-%d')} to {date_range.value[1].strftime('%Y-%m-%d')}  
**Metric:** {metric.value}
""")

# Query based on selections
if date_range.value and metric.value:
    query = f"""
    SELECT 
        date,
        {metric.value.lower()} as value
    FROM daily_metrics
    WHERE date BETWEEN %s AND %s
    ORDER BY date
    """
    
    df = pd.read_sql(
        query, 
        conn,
        params=[date_range.value[0], date_range.value[1]]
    )
    
    # Create chart
    chart = alt.Chart(df).mark_line(point=True).encode(
        x='date:T',
        y='value:Q',
        tooltip=['date', 'value']
    ).properties(
        width=700,
        height=400,
        title=f'{metric.value} Over Time'
    )
    
    mo.ui.altair_chart(chart)
```

## ⚡ Performance Tips

### 1. Use Connection Pooling

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from dbcreds import get_connection_string

# Create engine with connection pool
engine = create_engine(
    get_connection_string("prod"),
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10
)

# Reuse across queries
df1 = pd.read_sql("SELECT * FROM table1", engine)
df2 = pd.read_sql("SELECT * FROM table2", engine)
```

### 2. Cache Expensive Queries

```python
import marimo as mo
from functools import lru_cache
from dbcreds import get_connection_string
import pandas as pd

@lru_cache(maxsize=32)
def get_user_data(user_id: int) -> pd.DataFrame:
    conn = get_connection_string("prod")
    return pd.read_sql(
        "SELECT * FROM users WHERE id = %s",
        conn,
        params=[user_id]
    )

# Subsequent calls with same user_id are cached
user_id = mo.ui.number(1, 1000, 1, label="User ID")
df = get_user_data(user_id.value)
```

### 3. Async Queries for Better UX

```python
import marimo as mo
import asyncio
import pandas as pd
from dbcreds import get_connection_string

async def fetch_data_async(query: str):
    # In real app, use async database driver
    await asyncio.sleep(0.1)  # Simulate async work
    conn = get_connection_string("prod")
    return pd.read_sql(query, conn)

# Show loading state
with mo.status.spinner("Loading data..."):
    df = await fetch_data_async("SELECT * FROM large_table")
    
mo.md(f"Loaded {len(df):,} rows")
```

## 🛠️ Troubleshooting

### Still Getting Import Delays?

1. **Check marimo detection:**
   ```python
   import dbcreds
   print(f"Fast mode active: {dbcreds.USE_FAST_MODE}")
   print(f"Marimo detected: {dbcreds.IS_MARIMO}")
   ```

2. **Force fast mode:**
   ```python
   import os
   os.environ['DBCREDS_FAST_MODE'] = 'true'
   from dbcreds import get_connection_string
   ```

3. **Use direct fast import:**
   ```python
   from dbcreds.fast import get_connection_string
   ```

### Connection String Not Found?

Make sure credentials are stored in a fast-accessible location:

```bash
# Set environment variables (fastest)
export DBCREDS_PROD_HOST=localhost
export DBCREDS_PROD_PORT=5432
export DBCREDS_PROD_DATABASE=mydb
export DBCREDS_PROD_USERNAME=user
export DBCREDS_PROD_PASSWORD=pass

# Or use dbcreds CLI to store in credential manager
dbcreds add prod --host localhost --port 5432 ...
```

## 📚 More Examples

Find more marimo + dbcreds examples:

- [Data Analysis Notebooks](https://github.com/Sunnova-ShakesDlamini/dbcreds/tree/main/examples/marimo)
- [Interactive Dashboards](https://github.com/Sunnova-ShakesDlamini/dbcreds/tree/main/examples/dashboards)
- [ETL Pipelines](https://github.com/Sunnova-ShakesDlamini/dbcreds/tree/main/examples/etl)
