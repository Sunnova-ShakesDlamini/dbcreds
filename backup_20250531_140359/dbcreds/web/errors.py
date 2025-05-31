# dbcreds/web/errors.py
"""Error handling for the web interface."""

import sys
import traceback
from typing import Optional

from fastapi import Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.traceback import Traceback

from dbcreds.core.exceptions import (
    BackendError,
    CredentialError,
    CredentialNotFoundError,
    PasswordExpiredError,
    ValidationError,
)


class WebErrorHandler:
    """Rich error handler for web interface."""
    
    def __init__(self):
        """Initialize with a console for stderr output."""
        self.console = Console(stderr=True, force_terminal=True)
    
    def log_error(self, error: Exception, request: Optional[Request] = None) -> None:
        """Log error with rich formatting to console."""
        # Create error panel
        error_text = Text()
        error_text.append(f"{error.__class__.__name__}: ", style="bold red")
        error_text.append(str(error), style="red")
        
        if request:
            error_text.append(f"\n\nRequest: {request.method} {request.url}", style="dim")
        
        panel = Panel(
            error_text,
            title="[bold red]Web Server Error[/bold red]",
            border_style="red",
            padding=(1, 2),
        )
        self.console.print(panel)
        
        # Print rich traceback if debug mode
        if logger._core.min_level <= 10:  # DEBUG level
            tb = Traceback.from_exception(
                type(error),
                error,
                error.__traceback__,
                show_locals=True,
                suppress=[sys.modules[__name__]],
            )
            self.console.print(tb)
    
    def get_error_response(
        self, 
        request: Request, 
        error: Exception,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    ) -> HTMLResponse:
        """Get HTML error response for the web interface."""
        # Log the error
        self.log_error(error, request)
        
        # Determine error details
        if isinstance(error, CredentialNotFoundError):
            title = "Credential Not Found"
            message = str(error)
            status_code = status.HTTP_404_NOT_FOUND
            advice = "The requested credentials were not found. Please check the environment name."
        elif isinstance(error, PasswordExpiredError):
            title = "Password Expired"
            message = str(error)
            status_code = status.HTTP_403_FORBIDDEN
            advice = "The password for this environment has expired. Please update it."
        elif isinstance(error, ValidationError):
            title = "Validation Error"
            message = str(error)
            status_code = status.HTTP_400_BAD_REQUEST
            advice = "Please check your input and try again."
        elif isinstance(error, BackendError):
            title = "Backend Error"
            message = str(error)
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            advice = "The credential storage backend is unavailable. Please check system configuration."
        elif isinstance(error, CredentialError):
            title = "Credential Error"
            message = str(error)
            status_code = status.HTTP_400_BAD_REQUEST
            advice = "There was an error with the credential operation."
        else:
            title = "Internal Server Error"
            message = "An unexpected error occurred."
            advice = "Please try again later or contact support."
        
        # Create error HTML
        error_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Error - {title}</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-gray-100">
            <div class="min-h-screen flex items-center justify-center px-4">
                <div class="max-w-md w-full bg-white rounded-lg shadow-lg p-6">
                    <div class="flex items-center justify-center w-12 h-12 mx-auto bg-red-100 rounded-full">
                        <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </div>
                    <h1 class="mt-4 text-xl font-semibold text-center text-gray-900">{title}</h1>
                    <p class="mt-2 text-center text-gray-600">{message}</p>
                    <p class="mt-4 text-sm text-center text-gray-500">{advice}</p>
                    <div class="mt-6">
                        <button onclick="window.history.back()" class="w-full px-4 py-2 text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500">
                            Go Back
                        </button>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return HTMLResponse(content=error_html, status_code=status_code)


# Global error handler instance
web_error_handler = WebErrorHandler()