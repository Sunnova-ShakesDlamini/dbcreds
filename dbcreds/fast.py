# dbcreds/fast.py
"""
Fast, lightweight credential access for environments like marimo notebooks.

This module provides direct credential access without initializing the full
dbcreds infrastructure.
"""

import os
import ctypes
import ctypes.wintypes
import json
from typing import Dict, Any, Optional


def get_connection_string(environment: str) -> str:
    """
    Get database connection string using fast, lightweight method.
    
    This bypasses all dbcreds initialization and directly reads from
    environment variables or Windows Credential Manager.
    
    Args:
        environment: Environment name
        
    Returns:
        Database connection URI
        
    Raises:
        ValueError: If credentials not found
    """
    # Check environment variables first
    conn_string = _get_from_environment(environment)
    if conn_string:
        return conn_string
    
    # Fall back to Windows Credential Manager
    if os.name == 'nt':
        conn_string = _get_from_windows_credential_manager(environment)
        if conn_string:
            return conn_string
    
    raise ValueError(
        f"No credentials found for environment '{environment}'. "
        "Please ensure credentials are set in environment variables or Windows Credential Manager."
    )


def _get_from_environment(env_name: str) -> Optional[str]:
    """Try to get connection from environment variables."""
    # Check if dbcreds has set environment variables
    prefix = f"DBCREDS_{env_name.upper()}_"
    
    # Also check legacy format (for PowerShell compatibility)
    legacy_vars = {
        'host': os.environ.get('DB_SERVER'),
        'port': os.environ.get('DB_PORT', '5432'),
        'database': os.environ.get('DB_NAME'),
        'username': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PWD'),
    }
    
    # Check new format
    new_vars = {
        'host': os.environ.get(f'{prefix}HOST'),
        'port': os.environ.get(f'{prefix}PORT', '5432'),
        'database': os.environ.get(f'{prefix}DATABASE'),
        'username': os.environ.get(f'{prefix}USERNAME'),
        'password': os.environ.get(f'{prefix}PASSWORD'),
    }
    
    # Use whichever has data
    vars_to_use = new_vars if new_vars['host'] else legacy_vars
    
    if all(vars_to_use.get(k) for k in ['host', 'database', 'username']):
        # Password might be in credential manager, but try env first
        if not vars_to_use.get('password') and os.name == 'nt':
            # Try to get from Windows Credential Manager
            cred_data = _read_windows_credential(f"dbcreds:{env_name}")
            if cred_data and cred_data.get('password'):
                vars_to_use['password'] = cred_data['password']
        
        if vars_to_use.get('password'):
            return (
                f"postgresql://{vars_to_use['username']}:{vars_to_use['password']}"
                f"@{vars_to_use['host']}:{vars_to_use['port']}/{vars_to_use['database']}"
            )
    
    return None


def _get_from_windows_credential_manager(env_name: str) -> Optional[str]:
    """Get connection string from Windows Credential Manager."""
    if os.name != 'nt':
        return None
    
    cred_data = _read_windows_credential(f"dbcreds:{env_name}")
    if cred_data and all(k in cred_data for k in ['username', 'password', 'host', 'database']):
        return (
            f"postgresql://{cred_data['username']}:{cred_data['password']}"
            f"@{cred_data['host']}:{cred_data.get('port', 5432)}/{cred_data['database']}"
        )
    
    return None


def _read_windows_credential(target: str) -> Dict[str, Any]:
    """Read credential from Windows Credential Manager using ctypes."""
    if os.name != 'nt':
        return {}
    
    class CREDENTIAL(ctypes.Structure):
        _fields_ = [
            ("Flags", ctypes.wintypes.DWORD),
            ("Type", ctypes.wintypes.DWORD),
            ("TargetName", ctypes.wintypes.LPWSTR),
            ("Comment", ctypes.wintypes.LPWSTR),
            ("LastWritten", ctypes.wintypes.FILETIME),
            ("CredentialBlobSize", ctypes.wintypes.DWORD),
            ("CredentialBlob", ctypes.POINTER(ctypes.c_char)),
            ("Persist", ctypes.wintypes.DWORD),
            ("AttributeCount", ctypes.wintypes.DWORD),
            ("Attributes", ctypes.c_void_p),
            ("TargetAlias", ctypes.wintypes.LPWSTR),
            ("UserName", ctypes.wintypes.LPWSTR),
        ]
    
    advapi32 = ctypes.windll.advapi32
    cred_ptr = ctypes.POINTER(CREDENTIAL)()
    
    CRED_TYPE_GENERIC = 1
    
    # Try to read the credential
    if advapi32.CredReadW(target, CRED_TYPE_GENERIC, 0, ctypes.byref(cred_ptr)):
        try:
            cred = cred_ptr.contents
            username = cred.UserName if cred.UserName else ""
            
            # Extract password from blob
            blob_size = cred.CredentialBlobSize
            if blob_size > 0:
                # Read the blob data
                blob_data = ctypes.string_at(cred.CredentialBlob, blob_size)
                
                # Try to decode as JSON first (dbcreds format)
                try:
                    blob_str = blob_data.decode('utf-16le', errors='ignore').rstrip('\x00')
                    data = json.loads(blob_str)
                    password = data.get('password', '')
                    
                    # Get other metadata
                    return {
                        'username': username,
                        'password': password,
                        'host': data.get('host', ''),
                        'port': data.get('port', 5432),
                        'database': data.get('database', ''),
                    }
                except (json.JSONDecodeError, UnicodeDecodeError):
                    # Fallback: treat entire blob as password
                    password = blob_data.decode('utf-16le', errors='ignore').rstrip('\x00')
                    return {
                        'username': username,
                        'password': password
                    }
            
            return {'username': username, 'password': ''}
            
        finally:
            advapi32.CredFree(cred_ptr)
    
    return {}


# Convenience aliases
get = get_connection_string
fast_get = get_connection_string