```bash
# Install dbcreds
pip install git+https://github.com/Sunnova-ShakesDlamini/dbcreds.git

# Initialize and add your first environment
dbcreds init
dbcreds add dev --type postgresql

# Use in your Python code
from dbcreds import get_engine
engine = get_engine("dev")
```