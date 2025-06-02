# Security Best Practices

Follow these best practices to ensure your database credentials remain secure.

## 🔐 Credential Storage

### Use System Credential Stores

dbcreds automatically uses the most secure storage available:

- **Windows**: Windows Credential Manager
- **macOS**: Keychain
- **Linux**: Secret Service (GNOME Keyring, KWallet)

### Avoid Plain Text Storage

Never store credentials in:
- Code files
- Configuration files (without encryption)
- Environment files in repositories
- Shared documents

## 🔑 Password Management

### Regular Rotation

Set up password expiration:

```python
from dbcreds import CredentialManager

manager = CredentialManager()
manager.set_credentials(
    "prod",
    host="db.company.com",
    port=5432,
    database="production",
    username="app_user",
    password="new_secure_password",
    password_expires_days=90  # Expire after 90 days
)
```

Check for expiring passwords:

```bash
dbcreds check

⚠️  Expiring Soon:
  - prod: 5 days remaining
  - staging: 12 days remaining
```

### Strong Password Policy

- Minimum 16 characters
- Mix of uppercase, lowercase, numbers, symbols
- Unique per environment
- No dictionary words or patterns

## 🛡️ Access Control

### Principle of Least Privilege

Create database users with minimal required permissions:

```sql
-- Read-only user for analytics
CREATE USER analytics_reader WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE production TO analytics_reader;
GRANT USAGE ON SCHEMA public TO analytics_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analytics_reader;

-- Application user with specific permissions
CREATE USER app_user WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE production TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE users, orders TO app_user;
```

### Environment Separation

```python
# Separate credentials per environment
environments = ["dev", "staging", "prod"]

for env in environments:
    manager.add_environment(
        env,
        DatabaseType.POSTGRESQL,
        is_production=(env == "prod")
    )
    
# Use different users per environment
# dev_user, staging_user, prod_user
```

## 🔍 Audit & Monitoring

### Connection Logging

Enable connection logging in production:

```python
import logging
from dbcreds import get_engine

# Set up audit logging
logging.basicConfig(
    filename='db_connections.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(message)s'
)

logger = logging.getLogger('db_audit')

# Log connections
engine = get_engine("prod", echo=True)
logger.info(f"Database connection established to production")
```

### Failed Authentication Monitoring

Monitor failed authentication attempts:

```sql
-- PostgreSQL: Check failed login attempts
SELECT 
    usename,
    client_addr,
    error_severity,
    error_message,
    timestamp
FROM postgres_log
WHERE error_message LIKE '%authentication failed%'
ORDER BY timestamp DESC
LIMIT 100;
```

## 🚫 What NOT to Do

### Don't Commit Credentials

```bash
# Bad: .env file with credentials
DB_PASSWORD=mysecretpassword

# Good: .env.example file
DB_PASSWORD=your_password_here
```

Add to `.gitignore`:
```
.env
.env.local
*.pem
*.key
config/secrets.yml
```

### Don't Share Credentials

Instead of sharing passwords:

```bash
# Each developer sets up their own
dbcreds add dev --host localhost --port 5432 --database devdb --username $USER
```

### Don't Use Production Data in Development

```python
# Bad: Using production credentials in dev
conn = get_connection_string("prod")

# Good: Use sanitized development data
conn = get_connection_string("dev")
```

## 🔄 Secure Credential Rotation

### Automated Rotation Script

```python
import secrets
import string
from datetime import datetime
from dbcreds import CredentialManager
import psycopg2
from psycopg2.sql import SQL, Identifier

def generate_secure_password(length=24):
    """Generate a cryptographically secure password."""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(characters) for _ in range(length))

def rotate_password(environment: str):
    """Rotate database password for an environment."""
    manager = CredentialManager()
    
    # Get current credentials
    old_creds = manager.get_credentials(environment)
    
    # Generate new password
    new_password = generate_secure_password()
    
    # Update database password
    admin_conn = psycopg2.connect(
        host=old_creds.host,
        port=old_creds.port,
        database="postgres",
        user="admin_user",
        password="admin_password"
    )
    
    with admin_conn.cursor() as cur:
        cur.execute(
            SQL("ALTER USER {} WITH PASSWORD %s").format(
                Identifier(old_creds.username)
            ),
            [new_password]
        )
    
    admin_conn.commit()
    admin_conn.close()
    
    # Update stored credentials
    manager.set_credentials(
        environment,
        host=old_creds.host,
        port=old_creds.port,
        database=old_creds.database,
        username=old_creds.username,
        password=new_password,
        password_expires_days=90
    )
    
    print(f"✅ Password rotated for {environment}")
    print(f"   Next rotation: 90 days")

# Rotate production password
rotate_password("prod")
```

## 🔒 Network Security

### Use SSL/TLS Connections

```python
from dbcreds import get_engine

# Require SSL for production
engine = get_engine(
    "prod",
    connect_args={
        "sslmode": "require",
        "sslcert": "/path/to/client-cert.pem",
        "sslkey": "/path/to/client-key.pem",
        "sslrootcert": "/path/to/ca-cert.pem"
    }
)
```

### IP Whitelisting

Configure database firewall rules:

```sql
-- PostgreSQL: pg_hba.conf
# TYPE  DATABASE  USER        ADDRESS          METHOD
host    all       prod_user   10.0.0.0/24     md5
host    all       prod_user   192.168.1.0/24  md5
hostssl all       prod_user   0.0.0.0/0       cert
```

## 🚨 Incident Response

### If Credentials Are Compromised

1. **Immediately rotate the password**
   ```bash
   dbcreds update prod --password
   ```

2. **Check access logs**
   ```sql
   -- PostgreSQL: Recent connections
   SELECT 
       datname,
       usename,
       client_addr,
       backend_start,
       state
   FROM pg_stat_activity
   WHERE backend_start > NOW() - INTERVAL '24 hours'
   ORDER BY backend_start DESC;
   ```

3. **Revoke compromised credentials**
   ```sql
   -- Revoke access
   REVOKE CONNECT ON DATABASE production FROM compromised_user;
   
   -- Terminate existing connections
   SELECT pg_terminate_backend(pid)
   FROM pg_stat_activity
   WHERE usename = 'compromised_user';
   ```

4. **Audit recent changes**
   ```sql
   -- Check for unauthorized changes
   SELECT *
   FROM audit_log
   WHERE user_name = 'compromised_user'
     AND timestamp > NOW() - INTERVAL '7 days'
   ORDER BY timestamp DESC;
   ```

## 📋 Security Checklist

- [ ] Credentials stored in secure system store (not plain text)
- [ ] Password rotation enabled (90 days or less)
- [ ] Strong passwords (16+ characters, complex)
- [ ] Principle of least privilege for database users
- [ ] SSL/TLS enabled for connections
- [ ] IP whitelisting configured
- [ ] Audit logging enabled
- [ ] Regular security reviews scheduled
- [ ] Incident response plan documented
- [ ] No credentials in version control
- [ ] Development uses separate credentials from production
