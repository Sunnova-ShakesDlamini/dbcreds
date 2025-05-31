# Security Backends

## Backend Security

Each backend provides different security guarantees:

### Keyring Backend
- Uses OS-native credential storage
- Encrypted at rest
- User-level isolation

### Windows Credential Manager
- Windows DPAPI encryption
- Integrated with Windows security

### Environment Variables
- No encryption
- Suitable for containers
- Should use secrets management

## Backend Interface

See the [Backend API Reference](../api/backends.md) for implementation details.
