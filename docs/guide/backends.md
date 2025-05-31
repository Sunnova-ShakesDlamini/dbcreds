# Storage Backends

dbcreds supports multiple credential storage backends.

## Available Backends

### Keyring Backend
Cross-platform using system credential stores.

### Windows Credential Manager
Native Windows credential storage.

### Environment Variables
Read credentials from environment.

### Config File
JSON file storage (metadata only).

## Backend Priority

Backends are tried in order of security and availability.

See [Backend API](../api/backends.md) for implementation details.
