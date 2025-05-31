# dbcreds/core/models.py
"""
Pydantic models for database credentials.

This module defines the data models used throughout dbcreds for type safety
and validation.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, SecretStr, field_validator


class DatabaseType(str, Enum):
    """Supported database types."""

    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    ORACLE = "oracle"
    MSSQL = "mssql"
    SQLITE = "sqlite"


class Environment(BaseModel):
    """
    Database environment configuration.

    Represents a named database environment (e.g., dev, staging, prod) with
    its associated settings.

    Attributes:
        name: Environment name (e.g., 'dev', 'prod')
        database_type: Type of database
        description: Optional description of the environment
        is_production: Whether this is a production environment
        created_at: When the environment was created
        updated_at: When the environment was last updated
    """

    name: str = Field(..., min_length=1, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")
    database_type: DatabaseType
    description: Optional[str] = None
    is_production: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate environment name."""
        return v.lower()


class DatabaseCredentials(BaseModel):
    """
    Database connection credentials.

    Secure storage model for database connection information.

    Attributes:
        environment: Environment name
        host: Database server hostname or IP
        port: Database server port
        database: Database name
        username: Database username
        password: Database password (stored securely)
        options: Additional connection options
        ssl_mode: SSL connection mode
        password_updated_at: When the password was last updated
        password_expires_at: When the password expires
    """

    environment: str
    host: str
    port: int = Field(..., gt=0, le=65535)
    database: str
    username: str
    password: SecretStr
    options: Dict[str, Any] = Field(default_factory=dict)
    ssl_mode: Optional[str] = None
    password_updated_at: datetime = Field(default_factory=datetime.utcnow)
    password_expires_at: Optional[datetime] = None

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int, info) -> int:
        """Set default port based on database type if not specified."""
        if v is None and hasattr(info, "context") and "database_type" in info.context:
            db_type = info.context["database_type"]
            defaults = {
                DatabaseType.POSTGRESQL: 5432,
                DatabaseType.MYSQL: 3306,
                DatabaseType.ORACLE: 1521,
                DatabaseType.MSSQL: 1433,
            }
            return defaults.get(db_type, v)
        return v

    def get_connection_string(self, include_password: bool = True, driver: Optional[str] = None) -> str:
        """
        Generate a connection string for the database.

        Args:
            include_password: Whether to include the password in the connection string
            driver: Optional driver override for the connection string

        Returns:
            Database connection URI

        Examples:
            >>> creds.get_connection_string()
            'postgresql://user:pass@localhost:5432/mydb'
            >>> creds.get_connection_string(include_password=False)
            'postgresql://user@localhost:5432/mydb'
        """
        # This would be implemented based on database type
        # For now, return a PostgreSQL example
        password_part = f":{self.password.get_secret_value()}" if include_password else ""
        return f"postgresql://{self.username}{password_part}@{self.host}:{self.port}/{self.database}"

    def is_password_expired(self) -> bool:
        """Check if the password has expired."""
        if self.password_expires_at is None:
            return False
        return datetime.utcnow() > self.password_expires_at

    def days_until_expiry(self) -> Optional[int]:
        """Get the number of days until password expiry."""
        if self.password_expires_at is None:
            return None
        delta = self.password_expires_at - datetime.utcnow()
        return max(0, delta.days)  # Return 0 if already expired


class CredentialMetadata(BaseModel):
    """
    Metadata about stored credentials.

    Tracks additional information about credentials for management purposes.

    Attributes:
        environment: Environment name
        created_by: User who created the credentials
        created_at: When the credentials were created
        last_accessed: When the credentials were last accessed
        access_count: Number of times accessed
        last_tested: When the connection was last tested
        last_test_success: Whether the last test was successful
    """

    environment: str
    created_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_accessed: Optional[datetime] = None
    access_count: int = 0
    last_tested: Optional[datetime] = None
    last_test_success: Optional[bool] = None
