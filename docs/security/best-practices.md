# Security Best Practices

This guide covers security best practices for using dbcreds in production environments.

## Credential Storage

### Use System Credential Stores

dbcreds automatically uses the most secure credential storage available:

- **Windows**: Windows Credential Manager
- **macOS**: Keychain
- **Linux**: Secret Service (libsecret)

Never store credentials in:
- Plain text files
- Environment variables (except for containers)
- Source code
- Version control

### Backend Priority

dbcreds tries backends in this order:
1. Platform-specific secure storage (Windows Credential Manager, Keychain)
2. Cross-platform keyring
3. Environment variables (for containers)
4. Configuration files (metadata only, no passwords)

## Web Interface Security

### Authentication

The web interface requires authentication. Change the default credentials immediately:

```python
# dbcreds/web/auth.py
DEFAULT_USERNAME = "admin"  # Change this
DEFAULT_PASSWORD_HASH = pwd_context.hash("your-secure-password")  # Change this
```

### HTTPS Only

Always use HTTPS in production:

```bash
# Use a reverse proxy like nginx
dbcreds-server --host 127.0.0.1 --port 8001

# nginx configuration
server {
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Security Headers

dbcreds automatically sets security headers:
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Strict-Transport-Security: max-age=31536000

## Password Management

### Regular Rotation

Set password expiry policies:

```python
# Set 30-day expiry
manager.set_credentials(
    "production",
    host="db.example.com",
    port=5432,
    database="myapp",
    username="appuser",
    password="secure-password",
    password_expires_days=30  # Expire in 30 days
)
```

### Strong Passwords

Use strong, unique passwords:
- Minimum 16 characters
- Mix of uppercase, lowercase, numbers, symbols
- No dictionary words
- No personal information

Generate secure passwords:

```python
import secrets
import string

def generate_password(length=24):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))
```

## Access Control

### Principle of Least Privilege

- Create separate database users for different applications
- Grant only necessary permissions
- Use read-only accounts where possible

### Environment Isolation

```python
# Separate credentials for each environment
manager.add_environment("dev", DatabaseType.POSTGRESQL)
manager.add_environment("staging", DatabaseType.POSTGRESQL)
manager.add_environment("prod", DatabaseType.POSTGRESQL, is_production=True)
```

## Network Security

### Use SSL/TLS

Always encrypt database connections:

```python
# PostgreSQL with SSL
creds.options["sslmode"] = "require"
creds.options["sslcert"] = "/path/to/client-cert.pem"
creds.options["sslkey"] = "/path/to/client-key.pem"

# MySQL with SSL
creds.options["ssl_ca"] = "/path/to/ca.pem"
creds.options["ssl_cert"] = "/path/to/client-cert.pem"
creds.options["ssl_key"] = "/path/to/client-key.pem"
```

### IP Whitelisting

Restrict database access by IP:
- Use firewall rules
- Configure database server access controls
- Use VPN for remote access
