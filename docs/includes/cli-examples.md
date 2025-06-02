```bash
# Add a new environment
dbcreds add dev --type postgresql --host localhost --port 5432

# List environments  
dbcreds list

# Test connection
dbcreds test dev

# Update password
dbcreds update dev --password

# Check for expiring passwords
dbcreds check
```
