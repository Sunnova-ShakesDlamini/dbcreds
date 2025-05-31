# dbcreds/backends/legacy_windows.py
"""
Legacy Windows Credential Manager backend for existing credentials.

This backend reads credentials stored in the format used by the PowerShell profile.
"""

import ctypes
import json
import os
from typing import Any, Dict, Optional, Tuple

from loguru import logger

from dbcreds.backends.windows import CREDENTIAL, WindowsCredentialBackend
from dbcreds.core.models import DatabaseType


class LegacyWindowsBackend(WindowsCredentialBackend):
    """
    Backend for reading legacy Windows credentials stored by PowerShell profile.
    
    Reads credentials stored as:
    - Target: DBCredentials:{database_name}
    - Environment variables: DB_SERVER, DB_PORT, DB_NAME, DB_USER
    - JSON config at ~/.db_credentials/config.json
    """
    
    def __init__(self):
        """Initialize the legacy backend."""
        super().__init__()
        self.config_path = os.path.expanduser("~/.db_credentials/config.json")
    
    def get_credential(self, key: str) -> Optional[Tuple[str, str, Dict[str, Any]]]:
        """
        Retrieve credential from legacy storage.
        
        First tries dbcreds format, then falls back to legacy format.
        """
        # Try standard dbcreds format first
        result = super().get_credential(key)
        if result:
            return result
        
        # Extract environment name from key (e.g., "dbcreds:dev" -> "dev")
        if not key.startswith("dbcreds:"):
            return None
        
        env_name = key.split(":", 1)[1]
        
        # Try to find legacy credentials
        return self._get_legacy_credential(env_name)
    
    def _get_legacy_credential(self, env_name: str) -> Optional[Tuple[str, str, Dict[str, Any]]]:
        """Get credential from legacy PowerShell storage."""
        # First check if there's a JSON config file
        config = self._load_legacy_config()
        
        if config:
            # Try to get password from Windows Credential Manager using legacy format
            legacy_target = f"DBCredentials:{config.get('database', '')}"
            password = None
            
            try:
                password = self._get_password_from_legacy_target(legacy_target)
            except Exception as e:
                logger.debug(f"Could not get password from legacy target: {e}")
            
            if password:
                username = config.get("username", "")
                metadata = {
                    "host": config.get("server", "localhost"),
                    "port": int(config.get("port", 5432)),
                    "database": config.get("database", ""),
                    "password_updated_at": config.get("update_date", ""),
                    "password_expires_days": config.get("expiry_days", 90),
                }
                
                return (username, password, metadata)
        
        # Fall back to environment variables
        if all(os.environ.get(var) for var in ["DB_SERVER", "DB_PORT", "DB_NAME", "DB_USER"]):
            username = os.environ.get("DB_USER", "")
            password = os.environ.get("DB_PWD", "")
            
            # If no password in env, try legacy credential manager format
            if not password:
                db_name = os.environ.get("DB_NAME", "")
                legacy_target = f"DBCredentials:{db_name}"
                try:
                    password = self._get_password_from_legacy_target(legacy_target)
                except:
                    pass
            
            if password:
                metadata = {
                    "host": os.environ.get("DB_SERVER", "localhost"),
                    "port": int(os.environ.get("DB_PORT", 5432)),
                    "database": os.environ.get("DB_NAME", ""),
                    "password_updated_at": os.environ.get("DB_PWD_DATE", ""),
                    "password_expires_days": int(os.environ.get("DB_PWD_EXPIRY", 90)),
                }
                
                return (username, password, metadata)
        
        return None
    
    def _get_password_from_legacy_target(self, target: str) -> Optional[str]:
        """Get password using legacy target format."""
        cred_ptr = ctypes.POINTER(CREDENTIAL)()
        
        success = self.advapi32.CredReadW(
            target, 
            self.CRED_TYPE_GENERIC, 
            0, 
            ctypes.byref(cred_ptr)
        )
        
        if not success:
            return None
        
        try:
            cred = cred_ptr.contents
            
            # Extract password from credential blob
            blob_size = cred.CredentialBlobSize
            if blob_size > 0:
                blob_data = ctypes.string_at(cred.CredentialBlob, blob_size)
                # Legacy format stores password as UTF-16LE
                password = blob_data.decode("utf-16le", errors="ignore").rstrip("\x00")
                return password
            
            return None
        finally:
            self.advapi32.CredFree(cred_ptr)
    
    def _load_legacy_config(self) -> Optional[Dict[str, Any]]:
        """Load legacy configuration from JSON file."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.debug(f"Could not load legacy config: {e}")
        
        return None