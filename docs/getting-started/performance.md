# Performance & Lazy Loading

dbcreds v2.0 introduces intelligent lazy loading to ensure fast imports and optimal performance, especially in environments like Jupyter and marimo notebooks.

## 🚀 Fast Mode

### Automatic Detection

dbcreds automatically detects when it's running in a marimo notebook and switches to fast mode:

```python
# In marimo - no configuration needed!
from dbcreds import get_connection_string
conn_string = get_connection_string("prod")  # Lightning fast!
```

### Manual Fast Mode

You can enable fast mode anywhere using an environment variable:

```bash
export DBCREDS_FAST_MODE=true
python your_script.py
```

Or programmatically:

```python
import os
os.environ['DBCREDS_FAST_MODE'] = 'true'

from dbcreds import get_connection_string
conn_string = get_connection_string("prod")
```

### Direct Fast Access

Use the dedicated fast function to bypass all initialization:

```python
from dbcreds import get_connection_string_fast
conn_string = get_connection_string_fast("prod")
```

## ⚡ How It Works

### Lazy Module Loading

dbcreds uses Python's `__getattr__` to defer imports until actually needed:

```python
# This doesn't load anything heavy
import dbcreds

# Only loads what's needed when you use it
conn_string = dbcreds.get_connection_string("prod")
```

### Credential Resolution Order

In fast mode, dbcreds checks credentials in this order:

1. **Environment Variables** (fastest)
   - `DBCREDS_ENV_*` format
   - Legacy `DB_*` format (PowerShell compatibility)

2. **Windows Credential Manager** (Windows only)
   - Direct API access without backend initialization

3. **Error** if not found

### Performance Comparison

```python
# Standard mode (full initialization)
# Import time: ~0.8-1.2 seconds
from dbcreds import CredentialManager
manager = CredentialManager()

# Fast mode (lazy loading)
# Import time: ~0.05-0.1 seconds
from dbcreds import get_connection_string
conn_string = get_connection_string("prod")
```

## 🎯 When to Use Each Mode

### Use Fast Mode When:

- Working in Jupyter/marimo notebooks
- Building CLI tools that need quick startup
- Only need connection strings (not full credential management)
- Running in CI/CD pipelines
- Building microservices with tight startup constraints

### Use Standard Mode When:

- Managing credentials (add/update/remove)
- Using the web interface
- Running credential rotation
- Testing connections
- Accessing full credential metadata

## 🔧 Configuration

### Environment Variables

Control dbcreds behavior with environment variables:

```bash
# Enable fast mode globally
export DBCREDS_FAST_MODE=true

# Enable debug logging (standard mode only)
export DBCREDS_DEBUG=true

# Custom config directory
export DBCREDS_CONFIG_DIR=/custom/path
```

### Programmatic Control

```python
# Check if in fast mode
import dbcreds
if dbcreds.USE_FAST_MODE:
    print("Running in fast mode!")

# Force standard mode even in marimo
import os
os.environ['DBCREDS_FAST_MODE'] = 'false'
import dbcreds  # Full initialization
```

## 📊 Benchmarks

Typical import times on modern hardware:

| Mode | Import Time | Memory Usage |
|------|------------|--------------|
| Standard Mode | 0.8-1.2s | ~25MB |
| Fast Mode | 0.05-0.1s | ~5MB |
| Direct Fast | 0.02-0.05s | ~3MB |

## 🛠️ Troubleshooting

### Import Still Slow?

1. Ensure you're using the latest version:
   ```bash
   pip install --upgrade dbcreds
   ```

2. Check if fast mode is active:
   ```python
   import dbcreds
   print(f"Fast mode: {dbcreds.USE_FAST_MODE}")
   ```

3. Use direct fast access:
   ```python
   from dbcreds.fast import get_connection_string
   ```

### Fast Mode Limitations

In fast mode, these features are not available:

- `CredentialManager` class
- Credential add/update/remove operations  
- Web interface
- Connection testing
- Password rotation checks

To use these features, disable fast mode:

```python
import os
os.environ['DBCREDS_FAST_MODE'] = 'false'
from dbcreds import CredentialManager
```

## 🔍 Debugging Performance

Enable timing logs to debug import performance:

```python
import time
start = time.time()
from dbcreds import get_connection_string
print(f"Import took {time.time() - start:.3f}s")

# More detailed timing
import sys
import importlib

def time_import(module_name):
    start = time.time()
    module = importlib.import_module(module_name)
    elapsed = time.time() - start
    print(f"{module_name}: {elapsed:.3f}s")
    return module

# Time individual components
time_import('dbcreds')
time_import('dbcreds.core')
time_import('dbcreds.utils.shortcuts')
```
