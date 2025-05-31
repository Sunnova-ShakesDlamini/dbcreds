# Migration Guide

## From PowerShell Profile

If you have existing credentials in PowerShell, use the migration tool:

```bash
dbcreds-migrate --name dev
```

This will import credentials from:
- Environment variables (`DB_SERVER`, `DB_PORT`, etc.)
- Windows Credential Manager
- JSON config at `~/.db_credentials/config.json`

## Manual Migration

::: dbcreds.migrate
    options:
      show_source: false
