# Password Rotation

## Automatic Expiry Tracking

dbcreds tracks password age and expiry:

```python
from dbcreds import get_credentials

creds = get_credentials("dev")
days_left = creds.days_until_expiry()
if creds.is_password_expired():
    print("Password expired!")
```

## Setting Expiry

```bash
# Set 90-day expiry
dbcreds add dev --expires-days 90

# Update expiry
dbcreds update dev --expires-days 180
```

## Checking Status

```bash
# Check all environments
dbcreds check
```
