# dbcreds/web/security_config.py
"""
Security configuration and best practices for the web interface.
"""

import os
from typing import Dict, Any

from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware


def get_security_headers() -> Dict[str, str]:
    """
    Get security headers for HTTP responses.
    
    Returns:
        Dictionary of security headers
    """
    return {
        # Prevent XSS attacks
        "X-XSS-Protection": "1; mode=block",
        "X-Content-Type-Options": "nosniff",
        
        # Prevent clickjacking
        "X-Frame-Options": "DENY",
        
        # Content Security Policy - Allow CDN resources for UI frameworks
        "Content-Security-Policy": (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://unpkg.com https://cdn.tailwindcss.com https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://fonts.googleapis.com; "
            "img-src 'self' data: https:; "
            "font-src 'self' data: https://fonts.gstatic.com; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        ),
        
        # Referrer Policy
        "Referrer-Policy": "strict-origin-when-cross-origin",
        
        # Permissions Policy
        "Permissions-Policy": (
            "geolocation=(), "
            "microphone=(), "
            "camera=(), "
            "payment=(), "
            "usb=(), "
            "magnetometer=(), "
            "gyroscope=(), "
            "accelerometer=()"
        ),
    }


def configure_https_redirect(app, force_https: bool = False):
    """
    Configure HTTPS redirect middleware.
    
    Args:
        app: FastAPI application
        force_https: Force HTTPS in production
    """
    if force_https or os.getenv("DBCREDS_FORCE_HTTPS", "").lower() == "true":
        @app.middleware("http")
        async def redirect_to_https(request: Request, call_next):
            if request.url.scheme == "http":
                url = request.url.replace(scheme="https")
                return Response(
                    content="",
                    status_code=301,
                    headers={"Location": str(url)}
                )
            
            response = await call_next(request)
            
            # Add HSTS header for HTTPS connections
            response.headers["Strict-Transport-Security"] = (
                "max-age=63072000; includeSubDomains; preload"
            )
            
            return response


def sanitize_log_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize sensitive data before logging.
    
    Args:
        data: Dictionary containing potentially sensitive data
        
    Returns:
        Sanitized dictionary safe for logging
    """
    sensitive_keys = {
        'password', 'passwd', 'pwd', 'secret', 'token', 
        'api_key', 'apikey', 'auth', 'authorization',
        'cookie', 'session', 'credit_card', 'ssn'
    }
    
    sanitized = data.copy()
    
    for key in list(sanitized.keys()):
        # Check if key contains sensitive terms
        if any(term in key.lower() for term in sensitive_keys):
            sanitized[key] = '***REDACTED***'
    
    return sanitized


# Security recommendations as constants
SECURITY_RECOMMENDATIONS = """
# DBCreds Web Interface Security Recommendations

## 1. ALWAYS Use HTTPS in Production
- Set DBCREDS_FORCE_HTTPS=true environment variable
- Use a reverse proxy (nginx/Apache) with SSL certificates
- Never transmit passwords over HTTP

## 2. Authentication
- Change default admin password immediately
- Use strong passwords (min 12 characters)
- Consider implementing MFA (multi-factor authentication)
- Rotate passwords regularly

## 3. Network Security
- Bind to localhost (127.0.0.1) only if not needed externally
- Use firewall rules to restrict access
- Consider VPN for remote access
- Implement rate limiting

## 4. Logging
- Never log passwords or sensitive data
- Rotate logs regularly
- Store logs securely
- Monitor for suspicious activity

## 5. Environment Variables
Example secure configuration:
```bash
export DBCREDS_FORCE_HTTPS=true
export DBCREDS_BIND_HOST=127.0.0.1
export DBCREDS_SECRET_KEY=$(openssl rand -hex 32)
export DBCREDS_ADMIN_PASSWORD_HASH=$(python -c "from passlib.context import CryptContext; print(CryptContext(schemes=['bcrypt']).hash('your-strong-password'))")
```

## 6. Production Deployment
- Use a reverse proxy (nginx recommended)
- Enable SSL/TLS with valid certificates
- Set secure headers in reverse proxy
- Implement request rate limiting
- Use a process manager (systemd/supervisor)

## 7. Example Nginx Configuration
```nginx
server {
    listen 443 ssl http2;
    server_name dbcreds.example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=63072000" always;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
"""


def print_security_warnings():
    """Print security warnings for development mode."""
    import sys
    from rich.console import Console
    from rich.panel import Panel
    
    console = Console()
    
    if os.getenv("DBCREDS_SUPPRESS_WARNINGS", "").lower() != "true":
        console.print(
            Panel.fit(
                "[bold yellow]⚠️  Security Warning[/bold yellow]\n"
                "[yellow]Running in development mode with HTTP.[/yellow]\n"
                "For production use:\n"
                "• Use HTTPS with valid SSL certificates\n"
                "• Change default admin credentials\n"
                "• Set DBCREDS_FORCE_HTTPS=true\n"
                "• See security_config.py for full recommendations",
                title="Security",
                border_style="yellow",
            )
        )