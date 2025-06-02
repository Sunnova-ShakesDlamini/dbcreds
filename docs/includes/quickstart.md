```bash
# Install
pip install dbcreds

# Add environment
dbcreds add prod --type postgresql

# Set credentials (stored securely)
dbcreds set prod --host db.company.com --port 5432 --database myapp --username dbuser

# Use in Python
from dbcreds import get_connection_string
conn_string = get_connection_string("prod")
```
