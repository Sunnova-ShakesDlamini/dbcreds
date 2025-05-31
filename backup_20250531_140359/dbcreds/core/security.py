# dbcreds/core/security.py
"""Security utilities for dbcreds."""

import re
from typing import Any, Dict

from dbcreds.core.exceptions import ValidationError


def sanitize_environment_name(name: str) -> str:
    """Sanitize environment name to prevent injection attacks."""
    if not re.match(r"^[a-zA-Z0-9_-]+$", name):
        raise ValidationError(
            "Environment name can only contain letters, numbers, hyphens, and underscores"
        )
    return name.lower()


def sanitize_connection_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize connection parameters."""
    # Remove any potentially dangerous keys
    dangerous_keys = ["password", "passwd", "pwd"]
    sanitized = {k: v for k, v in params.items() if k.lower() not in dangerous_keys}
    
    # Validate host
    if "host" in sanitized:
        if not re.match(r"^[a-zA-Z0-9.-]+$", sanitized["host"]):
            raise ValidationError("Invalid host format")
    
    # Validate port
    if "port" in sanitized:
        try:
            port = int(sanitized["port"])
            if not 1 <= port <= 65535:
                raise ValidationError("Port must be between 1 and 65535")
        except (ValueError, TypeError):
            raise ValidationError("Invalid port number")
    
    return sanitized


def mask_password(connection_string: str) -> str:
    """Mask password in connection strings for logging."""
    # Pattern to match passwords in various connection string formats
    patterns = [
        r"(password=)([^;]+)",
        r"(pwd=)([^;]+)",
        r"(:\/\/[^:]+:)([^@]+)(@)",
    ]
    
    masked = connection_string
    for pattern in patterns:
        masked = re.sub(pattern, r"\1****\3", masked, flags=re.IGNORECASE)
    
    return masked