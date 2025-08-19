# dbcreds/core/exceptions.py
"""
Custom exceptions for dbcreds.

This module defines all custom exceptions used throughout the package.
"""


class CredentialError(Exception):
    """Base exception for all credential-related errors."""

    pass


class CredentialNotFoundError(CredentialError):
    """Raised when requested credentials are not found."""

    pass


class PasswordExpiredError(CredentialError):
    """Raised when a password has expired."""

    pass


class BackendError(CredentialError):
    """Raised when a backend operation fails."""

    pass


class ValidationError(CredentialError):
    """Raised when credential validation fails."""

    pass


class SecurityError(CredentialError):
    """Raised when security operations fail."""

    pass


class AuditError(CredentialError):
    """Raised when audit operations fail."""

    pass