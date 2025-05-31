```bash
# Clone the repository
git clone https://github.com/Sunnova-ShakesDlamini/dbcreds.git
cd dbcreds

# Create virtual environment with uv
uv venv
uv pip install -e ".[dev]"

# Run tests
pytest

# Build documentation
mkdocs serve
```