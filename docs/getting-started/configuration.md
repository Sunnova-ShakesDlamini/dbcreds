# Configuration

## Configuration Directory

dbcreds stores its configuration in `~/.dbcreds/` by default.

## Environment Variables

You can override the configuration directory:

```bash
export DBCREDS_CONFIG_DIR=/path/to/config
```

## Backend Configuration

dbcreds automatically detects available backends. See [Backends](../security/backends.md) for details.
