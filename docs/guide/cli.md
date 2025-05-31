# CLI Reference

The `dbcreds` command provides a rich CLI for managing credentials.

## Commands

::: dbcreds.cli
    options:
      show_source: false
      members: false

## Usage Examples

### Initialize
```bash
dbcreds init
```

### Add Environment
```bash
dbcreds add dev --type postgresql
```

### List Environments
```bash
dbcreds list
```

### Show Details
```bash
dbcreds show dev
```

### Test Connection
```bash
dbcreds test dev
```

### Check Expiry
```bash
dbcreds check
```
