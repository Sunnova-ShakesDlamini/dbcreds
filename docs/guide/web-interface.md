# Web Interface

## Starting the Server

```bash
dbcreds-server
```

Visit http://localhost:8000

## Features

- Visual credential management
- Password expiry tracking
- Team collaboration
- Secure authentication

## Configuration

The web interface uses FastAPI and HTMX for a modern, responsive UI.

## API Endpoints

::: dbcreds.web.main
    options:
      show_source: false
      members:
        - app
        - index
        - create_environment
        - list_environments
