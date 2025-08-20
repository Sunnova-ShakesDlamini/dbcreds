#!/usr/bin/env python
"""Test script to verify the credential fix"""

from dbcreds.core.manager import CredentialManager

# Initialize manager
manager = CredentialManager()

# List environments
print("Available environments:")
for env in manager.list_environments():
    print(f"  - {env.name}")

# Try to get credentials for an environment
try:
    print("\nTrying to get credentials for 'ods-dev'...")
    creds = manager.get_credentials("ods-dev", check_expiry=False)
    print(f"  Success! Got credentials for {creds.environment}")
    print(f"  Username: {creds.username}")
except Exception as e:
    print(f"  Failed: {e}")

# Try to set credentials
try:
    print("\nTrying to set credentials for 'ods-dev'...")
    creds = manager.set_credentials(
        environment="ods-dev",
        host="localhost",
        port=5432,
        database="testdb",
        username="testuser",
        password="testpass123"
    )
    print(f"  Success! Saved credentials for {creds.environment}")
    
    # Now try to retrieve them again
    print("\nRetrieving saved credentials...")
    creds = manager.get_credentials("ods-dev", check_expiry=False)
    print(f"  Success! Retrieved credentials for {creds.environment}")
    print(f"  Host: {creds.host}")
    print(f"  Port: {creds.port}")
    print(f"  Database: {creds.database}")
    print(f"  Username: {creds.username}")
    
except Exception as e:
    print(f"  Failed: {e}")
    import traceback
    traceback.print_exc()

print("\nTest completed!")