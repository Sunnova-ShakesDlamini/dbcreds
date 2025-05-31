```bash
# List all environments
dbcreds list

# Show specific environment (without password)
dbcreds show dev

# Test connection
dbcreds test dev

# Update password
dbcreds update dev --password

# Remove environment
dbcreds remove dev

# Check password expiry
dbcreds check

# Export connection string
dbcreds export dev --format uri
```