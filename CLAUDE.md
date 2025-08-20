# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development Setup
```bash
# Install in development mode with all dependencies
uv pip install -e ".[dev]"

# Install with optional database drivers
uv pip install -e ".[dev,mysql,oracle,mssql]"
```

### Build and Test
```bash
# Run tests
make test               # Basic test run
pytest                  # Direct pytest
pytest --cov=dbcreds    # With coverage
pytest -m "not slow"    # Skip slow tests

# Linting and formatting
make lint               # Run all linters (ruff, black, mypy)
make format             # Auto-format code
ruff check --fix .      # Fix linting issues
mypy dbcreds            # Type checking

# Build
uv build                # Build wheel and sdist
make clean              # Clean build artifacts
```

### Documentation
```bash
make docs               # Build documentation
make serve-docs         # Serve docs locally at http://localhost:8000
mkdocs serve            # Alternative: direct MkDocs server
```

## Architecture

### Project Structure
- **dbcreds/**: Main package with lazy loading support for fast startup
  - **cli.py**: Typer-based CLI interface with rich terminal output
  - **backends/**: Storage backends (keyring, Windows credential store, etc.)
  - **core/**: Business logic (manager.py, models.py, security.py)
  - **web/**: FastAPI application with Jinja2 templates
  - **utils/**: Helper functions and shortcuts
- **tests/**: Comprehensive test suite organized by component
- **docs/**: MkDocs Material documentation

### Key Patterns
1. **Lazy Loading**: Modules loaded on-demand for performance. Fast mode available for notebooks.
2. **Backend Abstraction**: Multiple credential storage backends with common interface
3. **Type Safety**: Full Pydantic v2 validation and mypy type checking
4. **Async Support**: Both sync and async APIs available

### Technology Stack
- **Python 3.8-3.12** with modern type hints
- **FastAPI** for web interface and REST API
- **Typer** for CLI with rich formatting
- **Pydantic v2** for data validation
- **SQLAlchemy 2.0** for database ORM
- **Keyring** for secure credential storage
- **uv** for fast package management

### Testing Strategy
- pytest with async support
- Test markers: `slow`, `integration`, `unit`
- Coverage reporting with HTML output
- Isolated testing with temporary directories
- FastAPI TestClient for web testing

### Security Considerations
- Credentials stored in OS-native secure storage (never plain text)
- Environment isolation (dev/staging/prod separation)
- Audit logging for credential access
- Automatic password rotation reminders

### Development Workflow
1. Make changes and ensure imports follow lazy loading pattern
2. Run `make format` before committing
3. Run `make lint` to check code quality
4. Run `make test` to verify functionality
5. Update documentation if adding new features
6. Use type hints and ensure `mypy` passes