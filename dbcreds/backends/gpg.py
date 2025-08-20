# dbcreds/backends/gpg.py
"""
GPG-based credential backend for enhanced security.

This backend provides GPG encryption for credentials, supporting:
- Multiple recipient keys for team access
- Signature verification for integrity
- Key rotation with automatic re-encryption
- Hardware security key support
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import gnupg
from loguru import logger

from dbcreds.backends.base import CredentialBackend
from dbcreds.core.exceptions import SecurityError, ValidationError


class GPGBackend(CredentialBackend):
    """
    GPG-encrypted credential storage backend.
    
    Provides strong encryption using GPG/PGP with support for
    multiple recipients, signature verification, and key rotation.
    """
    
    def __init__(self, 
                 storage_dir: Optional[Path] = None,
                 gpg_home: Optional[Path] = None,
                 default_recipients: Optional[List[str]] = None,
                 sign_key: Optional[str] = None):
        """
        Initialize GPG backend.
        
        Args:
            storage_dir: Directory for storing encrypted credentials
            gpg_home: GPG home directory (default: ~/.gnupg)
            default_recipients: Default GPG key IDs for encryption
            sign_key: GPG key ID for signing (optional)
        """
        self.storage_dir = storage_dir or Path.home() / ".dbcreds" / "gpg"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.gpg = gnupg.GPG(gnupghome=str(gpg_home) if gpg_home else None)
        self.default_recipients = default_recipients or []
        self.sign_key = sign_key
        
        # Verify GPG is available and keys exist
        self._verify_setup()
    
    def _verify_setup(self) -> None:
        """Verify GPG setup and key availability."""
        try:
            # Check GPG version
            version = self.gpg.version
            if not version:
                raise SecurityError("GPG not available or not properly configured")
            logger.debug(f"GPG version: {version}")
            
            # Verify default recipients have valid keys
            if self.default_recipients:
                keys = self.gpg.list_keys()
                key_ids = {k['keyid'] for k in keys}
                for recipient in self.default_recipients:
                    if recipient not in key_ids:
                        logger.warning(f"GPG key not found for recipient: {recipient}")
            
            # Verify signing key if specified
            if self.sign_key:
                secret_keys = self.gpg.list_keys(True)
                secret_key_ids = {k['keyid'] for k in secret_keys}
                if self.sign_key not in secret_key_ids:
                    raise SecurityError(f"Signing key not found: {self.sign_key}")
                    
        except Exception as e:
            logger.error(f"GPG setup verification failed: {e}")
            raise SecurityError(f"GPG backend initialization failed: {e}")
    
    def is_available(self) -> bool:
        """Check if GPG backend is available and functional."""
        try:
            # Test encryption/decryption
            test_data = "test"
            encrypted = self.gpg.encrypt(test_data, self.default_recipients)
            if not encrypted.ok:
                return False
            
            decrypted = self.gpg.decrypt(str(encrypted))
            return decrypted.ok and str(decrypted) == test_data
            
        except Exception as e:
            logger.debug(f"GPG backend not available: {e}")
            return False
    
    def _get_credential_path(self, key: str) -> Path:
        """Get the file path for a credential."""
        # Sanitize key for filesystem
        safe_key = "".join(c if c.isalnum() or c in "-_" else "_" for c in key)
        return self.storage_dir / f"{safe_key}.gpg"
    
    def _get_signature_path(self, key: str) -> Path:
        """Get the signature file path for a credential."""
        return Path(str(self._get_credential_path(key)) + ".sig")
    
    def get_credential(self, key: str) -> Optional[Tuple[str, str, Dict[str, Any]]]:
        """
        Retrieve and decrypt credential from GPG storage.
        
        Args:
            key: The credential identifier
            
        Returns:
            Tuple of (username, password, metadata) or None if not found
        """
        try:
            cred_path = self._get_credential_path(key)
            if not cred_path.exists():
                return None
            
            # Read encrypted data
            encrypted_data = cred_path.read_bytes()
            
            # Verify signature if it exists
            sig_path = self._get_signature_path(key)
            if sig_path.exists() and self.sign_key:
                signature = sig_path.read_bytes()
                verified = self.gpg.verify_data(signature, encrypted_data)
                if not verified.valid:
                    logger.warning(f"Invalid signature for credential: {key}")
                    raise SecurityError(f"Signature verification failed for {key}")
            
            # Decrypt data
            decrypted = self.gpg.decrypt(encrypted_data)
            if not decrypted.ok:
                logger.error(f"Failed to decrypt credential: {key}")
                return None
            
            # Parse JSON data
            data = json.loads(str(decrypted))
            username = data.pop("username", "")
            password = data.pop("password", "")
            
            return (username, password, data)
            
        except (json.JSONDecodeError, SecurityError) as e:
            logger.error(f"Failed to retrieve credential {key}: {e}")
            return None
    
    def set_credential(self, 
                      key: str, 
                      username: str, 
                      password: str, 
                      metadata: Dict[str, Any],
                      recipients: Optional[List[str]] = None) -> bool:
        """
        Encrypt and store credential with GPG.
        
        Args:
            key: The credential identifier
            username: Username for the credential
            password: Password for the credential
            metadata: Additional metadata
            recipients: Optional list of GPG recipients (uses defaults if None)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Prepare data
            data = {"username": username, "password": password, **metadata}
            json_data = json.dumps(data)
            
            # Determine recipients
            recipients = recipients or self.default_recipients
            if not recipients:
                raise ValidationError("No GPG recipients specified")
            
            # Encrypt data
            encrypted = self.gpg.encrypt(json_data, recipients, armor=False)
            if not encrypted.ok:
                logger.error(f"Encryption failed: {encrypted.status}")
                return False
            
            # Write encrypted data
            cred_path = self._get_credential_path(key)
            cred_path.write_bytes(encrypted.data)
            
            # Create signature if signing key is configured
            if self.sign_key:
                signature = self.gpg.sign(json_data, keyid=self.sign_key, detach=True)
                if signature:
                    sig_path = self._get_signature_path(key)
                    sig_path.write_bytes(signature.data)
            
            logger.info(f"Credential stored with GPG encryption: {key}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store credential {key}: {e}")
            return False
    
    def delete_credential(self, key: str) -> bool:
        """
        Delete credential and its signature.
        
        Args:
            key: The credential identifier
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cred_path = self._get_credential_path(key)
            sig_path = self._get_signature_path(key)
            
            deleted = False
            if cred_path.exists():
                cred_path.unlink()
                deleted = True
            
            if sig_path.exists():
                sig_path.unlink()
            
            return deleted
            
        except Exception as e:
            logger.error(f"Failed to delete credential {key}: {e}")
            return False
    
    def list_credentials(self) -> List[str]:
        """
        List all stored credentials.
        
        Returns:
            List of credential identifiers
        """
        try:
            credentials = []
            for path in self.storage_dir.glob("*.gpg"):
                # Remove .gpg extension and restore original key
                key = path.stem
                credentials.append(key)
            return sorted(credentials)
            
        except Exception as e:
            logger.error(f"Failed to list credentials: {e}")
            return []
    
    def rotate_keys(self, 
                   old_recipients: List[str],
                   new_recipients: List[str]) -> bool:
        """
        Re-encrypt all credentials with new recipients.
        
        Args:
            old_recipients: Current recipients (for decryption)
            new_recipients: New recipients (for re-encryption)
            
        Returns:
            True if all credentials rotated successfully
        """
        try:
            success_count = 0
            fail_count = 0
            
            for key in self.list_credentials():
                # Retrieve with current encryption
                result = self.get_credential(key)
                if not result:
                    logger.warning(f"Failed to decrypt credential for rotation: {key}")
                    fail_count += 1
                    continue
                
                username, password, metadata = result
                
                # Re-encrypt with new recipients
                if self.set_credential(key, username, password, metadata, new_recipients):
                    success_count += 1
                else:
                    fail_count += 1
            
            logger.info(f"Key rotation complete: {success_count} succeeded, {fail_count} failed")
            return fail_count == 0
            
        except Exception as e:
            logger.error(f"Key rotation failed: {e}")
            return False
    
    def verify_all_signatures(self) -> Dict[str, bool]:
        """
        Verify signatures for all stored credentials.
        
        Returns:
            Dictionary mapping credential keys to verification status
        """
        results = {}
        
        for key in self.list_credentials():
            cred_path = self._get_credential_path(key)
            sig_path = self._get_signature_path(key)
            
            if not sig_path.exists():
                results[key] = False
                continue
            
            try:
                encrypted_data = cred_path.read_bytes()
                signature = sig_path.read_bytes()
                
                # First decrypt to get original data
                decrypted = self.gpg.decrypt(encrypted_data)
                if not decrypted.ok:
                    results[key] = False
                    continue
                
                # Verify signature against decrypted data
                verified = self.gpg.verify_data(signature, str(decrypted).encode())
                results[key] = verified.valid
                
            except Exception as e:
                logger.error(f"Signature verification failed for {key}: {e}")
                results[key] = False
        
        return results
    
    def export_public_keys(self, recipients: Optional[List[str]] = None) -> str:
        """
        Export public keys for sharing with team members.
        
        Args:
            recipients: List of key IDs to export (default: all)
            
        Returns:
            ASCII-armored public keys
        """
        try:
            if recipients:
                return self.gpg.export_keys(recipients)
            else:
                return self.gpg.export_keys(self.gpg.list_keys())
                
        except Exception as e:
            logger.error(f"Failed to export public keys: {e}")
            return ""
    
    def import_public_keys(self, key_data: str) -> bool:
        """
        Import public keys from team members.
        
        Args:
            key_data: ASCII-armored public keys
            
        Returns:
            True if import successful
        """
        try:
            result = self.gpg.import_keys(key_data)
            logger.info(f"Imported {result.count} keys")
            return result.count > 0
            
        except Exception as e:
            logger.error(f"Failed to import public keys: {e}")
            return False