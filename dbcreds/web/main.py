# dbcreds/web/main.py
"""
FastAPI web application for dbcreds.

Provides a web interface for managing database credentials with
team collaboration features.
"""

import os
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install as install_rich_traceback

from dbcreds import __version__
from dbcreds.core.exceptions import CredentialError
from dbcreds.core.manager import CredentialManager
from dbcreds.core.models import DatabaseType
from dbcreds.web.errors import web_error_handler
from dbcreds.web.security_config import (
    get_security_headers,
    print_security_warnings,
    sanitize_log_data,
)

# Install rich traceback handler
install_rich_traceback(show_locals=True)

# Create console for startup messages
console = Console()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    console.print(
        Panel.fit(
            f"[bold green]dbcreds Web Server v{__version__}[/bold green]\n"
            f"[dim]Ready to manage your database credentials[/dim]",
            title="Starting Up",
            border_style="green",
        )
    )
    yield
    # Shutdown (if needed)


# Create FastAPI app
app = FastAPI(
    title="dbcreds Web",
    description="Database Credentials Management",
    version=__version__,
    lifespan=lifespan,
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # Configure for production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1"],  # Configure for production
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    # Add comprehensive security headers
    for header, value in get_security_headers().items():
        response.headers[header] = value
    return response


# Setup templates
templates_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# Mount static files
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


# Exception handlers
@app.exception_handler(CredentialError)
async def credential_error_handler(request: Request, exc: CredentialError):
    """Handle credential errors."""
    return web_error_handler.get_error_response(request, exc)


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions."""
    return web_error_handler.get_error_response(request, exc)


@app.exception_handler(HTTPException)
async def http_exception_handler_custom(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    # Log HTTP exceptions with rich formatting
    web_error_handler.log_error(exc, request)
    return await http_exception_handler(request, exc)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Home page."""
    try:
        manager = CredentialManager()
        environments = manager.list_environments()

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "title": "dbcreds",
                "environments": environments,
                "version": __version__,
            },
        )
    except Exception as e:
        logger.error(f"Error loading settings page: {e}")
        return HTMLResponse(
            content=f'<div class="text-red-600 p-4">Error loading settings: {str(e)}</div>',
            status_code=500,
        )


# Updated create_environment function for dbcreds/web/main.py


@app.post("/environments", response_class=HTMLResponse)
async def create_environment(request: Request):
    """Create a new environment."""
    try:
        form_data = await request.form()
        manager = CredentialManager()

        # Add the environment
        env_name = form_data.get("name", "").lower()
        db_type = DatabaseType(form_data.get("database_type"))

        manager.add_environment(
            env_name,
            db_type,
            description=form_data.get("description", ""),
            is_production=bool(form_data.get("is_production", False)),
        )

        # Get password update date if provided
        password_updated_at = None
        password_updated_at_str = form_data.get("password_updated_at", "").strip()
        if password_updated_at_str:
            try:
                # Parse as naive datetime then make timezone aware
                naive_dt = datetime.strptime(password_updated_at_str, "%Y-%m-%d")
                password_updated_at = naive_dt.replace(tzinfo=timezone.utc)
            except ValueError:
                # If parsing fails, use current date
                password_updated_at = None

        # Set credentials with the custom password_updated_at if provided
        expires_days = int(form_data.get("expires_days", 90))
        manager.set_credentials(
            env_name,
            host=form_data.get("host"),
            port=int(form_data.get("port", 5432)),
            database=form_data.get("database"),
            username=form_data.get("username"),
            password=form_data.get("password"),
            password_expires_days=expires_days,
            password_updated_at=password_updated_at,  # Pass the custom timestamp if provided
        )

        # Get updated environments list
        environments = manager.list_environments()

        # Return response with environment list, close modal, and show success
        return HTMLResponse(
            content=f"""
            <div id="environment-list" hx-swap-oob="true">
                {
                templates.get_template("partials/environment_list.html").render(
                    request=request, environments=environments
                )
            }
            </div>
            <div id="modal" hx-swap-oob="true"></div>
            <div id="notification-container" hx-swap-oob="afterbegin">
                <div class="fixed top-4 right-4 z-50 animate-fade-in-down">
                    <div class="bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded-lg shadow-lg flex items-center space-x-3">
                        <svg class="h-5 w-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                        </svg>
                        <span class="font-medium">Environment '{
                env_name
            }' created successfully!</span>
                    </div>
                </div>
                <script>
                    // Remove notification after 3 seconds
                    setTimeout(() => {{
                        const notification = document.querySelector('#notification-container > div');
                        if (notification) {{
                            notification.classList.add('animate-fade-out-up');
                            setTimeout(() => notification.remove(), 300);
                        }}
                    }}, 3000);
                    
                    // Reload expiry info for all environments
                    setTimeout(loadAllExpiryInfo, 100);
                </script>
            </div>
            """
        )
    except Exception as e:
        return HTMLResponse(
            content=f"""
            <div id="notification-container" hx-swap-oob="afterbegin">
                <div class="fixed top-4 right-4 z-50 animate-fade-in-down">
                    <div class="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg shadow-lg flex items-center space-x-3">
                        <svg class="h-5 w-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                        <span class="font-medium">Error: {str(e)}</span>
                    </div>
                </div>
                <script>
                    // Remove notification after 5 seconds
                    setTimeout(() => {{
                        const notification = document.querySelector('#notification-container > div');
                        if (notification) {{
                            notification.classList.add('animate-fade-out-up');
                            setTimeout(() => notification.remove(), 300);
                        }}
                    }}, 5000);
                </script>
            </div>
            """,
            status_code=400,
        )


@app.get("/environments", response_class=HTMLResponse)
async def list_environments(request: Request):
    """List all environments (HTMX endpoint)."""
    try:
        manager = CredentialManager()
        environments = manager.list_environments()

        return templates.TemplateResponse(
            "partials/environment_list.html",
            {
                "request": request,
                "environments": environments,
            },
        )
    except Exception as e:
        # Log the actual error
        console.print(f"[red]Error loading environments:[/red] {e}")
        if os.getenv("DBCREDS_DEBUG"):
            console.print_exception()

        # For HTMX requests, return a simple error partial
        return HTMLResponse(
            content=f'<div class="text-red-600 p-4">Error loading environments: {str(e)}</div>',
            status_code=500,
        )


@app.get("/settings", response_class=HTMLResponse)
async def settings(request: Request):
    """Settings page."""
    try:
        manager = CredentialManager()

        # Get backend information
        backends_info = []
        for backend in manager.backends:
            backend_name = backend.__class__.__name__
            backend_info = {
                "name": backend_name.replace("Backend", ""),
                "description": "",
                "available": backend.is_available(),
            }

            # Add descriptions for known backends
            if "Keyring" in backend_name:
                backend_info["description"] = (
                    "System keyring (Keychain on macOS, Credential Manager on Windows)"
                )
            elif "Windows" in backend_name:
                backend_info["description"] = "Windows Credential Manager"
            elif "Environment" in backend_name:
                backend_info["description"] = "Environment variables"
            elif "Config" in backend_name:
                backend_info["description"] = "JSON configuration files"

            backends_info.append(backend_info)

        return templates.TemplateResponse(
            "settings.html",
            {
                "request": request,
                "title": "Settings - dbcreds",
                "version": __version__,
                "config_dir": manager.config_dir,
                "backends": backends_info,
            },
        )
    except Exception:
        # Errors will be caught by exception handlers
        raise


@app.get("/environments/{env_name}/edit", response_class=HTMLResponse)
async def edit_environment_form(request: Request, env_name: str):
    """Get edit form for an environment."""
    try:
        manager = CredentialManager()
        creds = manager.get_credentials(env_name, check_expiry=False)
        env = next((e for e in manager.list_environments() if e.name == env_name), None)

        if not env:
            raise HTTPException(status_code=404, detail="Environment not found")

        # Helper function to ensure timezone-aware datetime
        def ensure_timezone_aware(dt):
            if dt and dt.tzinfo is None:
                return dt.replace(tzinfo=timezone.utc)
            return dt

        # Ensure datetimes are timezone-aware
        password_updated_at = ensure_timezone_aware(creds.password_updated_at)
        password_expires_at = ensure_timezone_aware(creds.password_expires_at)

        # Calculate days until expiry
        days_left = None
        expiry_period = 90  # Default

        if password_expires_at and password_updated_at:
            # Calculate the total expiry period (not the days left)
            expiry_period = (password_expires_at - password_updated_at).days
            # Calculate days left
            delta = password_expires_at - datetime.now(timezone.utc)
            days_left = delta.days if delta.days > 0 else 0
        elif password_updated_at:
            # If we have updated_at but no expires_at, still show it will expire
            # Calculate what the expiry date would be with default 90 days
            theoretical_expires_at = password_updated_at + timedelta(days=expiry_period)
            delta = theoretical_expires_at - datetime.now(timezone.utc)
            days_left = delta.days if delta.days > 0 else 0

        # Determine password status HTML
        if password_expires_at is None and password_updated_at:
            # Has update date but no expiry set - show calculated expiry
            password_status_html = f"""
            <span class="text-yellow-600">No expiry stored (would expire in {days_left} days)</span>
            """
        elif creds.is_password_expired():
            password_status_html = """
            <span class="text-red-600">Expired</span>
            """
        elif days_left is not None:
            if days_left <= 7:
                password_status_html = f"""
                <span class="text-red-600">{days_left} days remaining</span>
                """
            elif days_left <= 30:
                password_status_html = f"""
                <span class="text-yellow-600">{days_left} days remaining</span>
                """
            else:
                password_status_html = f"""
                <span class="text-green-600">{days_left} days remaining</span>
                """
        else:
            password_status_html = """
            <span class="text-gray-600">No expiry set</span>
            """

        # Add details about dates
        date_details_html = '<div class="text-xs text-gray-500 mt-1">'
        if password_updated_at:
            date_details_html += (
                f"Last updated: {password_updated_at.strftime('%Y-%m-%d')}"
            )
        if password_expires_at:
            date_details_html += (
                f"<br>Expires on: {password_expires_at.strftime('%Y-%m-%d')}"
            )
        elif password_updated_at and expiry_period > 0:
            theoretical_expires = password_updated_at + timedelta(days=expiry_period)
            date_details_html += f"<br>Would expire on: {theoretical_expires.strftime('%Y-%m-%d')} (not stored)"
        date_details_html += "</div>"

        html = f"""
        <div class="fixed z-10 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
            <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
                <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
                <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
                    <div>
                        <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                            Edit Environment: {env_name}
                        </h3>
                        <div class="mt-2">
                            <form method="POST" 
                                action="/environments/{env_name}"
                                hx-put="/environments/{env_name}" 
                                hx-target="#environment-list" 
                                hx-swap="innerHTML"
                                hx-indicator="#form-indicator"
                                hx-on::before-request="console.log('HTMX request starting')"
                                hx-on::after-request="console.log('HTMX request completed')"
                                hx-on::response-error="console.error('HTMX error:', event.detail)">
                                <!-- Add hidden loading indicator -->
                                <div id="form-indicator" class="htmx-indicator fixed inset-0 bg-gray-500 bg-opacity-50 flex items-center justify-center rounded-lg" style="display:none;">
                                    <div class="bg-white p-4 rounded-lg shadow-lg flex items-center space-x-3">
                                        <svg class="animate-spin h-5 w-5 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                        </svg>
                                        <span class="text-gray-700">Updating environment...</span>
                                    </div>
                                </div>
                                <div class="space-y-4">
                                    <div class="bg-gray-50 p-3 rounded-md">
                                        <label class="block text-sm font-medium text-gray-700 mb-2">
                                            Connection Details
                                        </label>
                                        <div class="text-sm text-gray-600 space-y-1">
                                            <div><span class="font-medium">Host:</span> {creds.host}:{creds.port}</div>
                                            <div><span class="font-medium">Database:</span> {creds.database}</div>
                                            <div><span class="font-medium">Username:</span> {creds.username}</div>
                                            <div><span class="font-medium">Type:</span> {env.database_type.value}</div>
                                        </div>
                                    </div>
                                    
                                    <div class="bg-blue-50 p-3 rounded-md">
                                        <label class="block text-sm font-medium text-gray-700 mb-2">
                                            Password Status
                                        </label>
                                        <div class="text-sm">
                                            <div class="mb-1">
                                                <span class="font-medium">Status:</span> {password_status_html}
                                            </div>
                                            {date_details_html}
                                        </div>
                                    </div>
                                    
                                    <div>
                                        <label for="current_password" class="block text-sm font-medium text-gray-700">
                                            Current Password
                                        </label>
                                        <div class="mt-1 relative">
                                            <input type="password" 
                                                   id="current_password" 
                                                   value="{creds.password.get_secret_value()}"
                                                   class="block w-full shadow-sm sm:text-sm border-gray-300 rounded-md bg-gray-100 pr-20"
                                                   readonly>
                                            <div class="absolute inset-y-0 right-0 flex items-center pr-2">
                                                <button type="button"
                                                        onclick="copyPassword('current_password')"
                                                        title="Copy password"
                                                        class="p-1 text-gray-400 hover:text-indigo-600">
                                                    <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                                    </svg>
                                                </button>
                                                <button type="button"
                                                        onclick="togglePasswordVisibility('current_password', 'eye_icon_current')"
                                                        title="Toggle visibility"
                                                        class="p-1 text-gray-400 hover:text-indigo-600">
                                                    <svg id="eye_icon_current" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                        <!-- Eye closed icon (default) -->
                                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                                                    </svg>
                                                </button>
                                            </div>
                                        </div>
                                        <p class="mt-1 text-xs text-gray-500">
                                            Password is stored securely ({len(creds.password.get_secret_value())} characters). Use icons to reveal or copy.
                                        </p>
                                        <div id="copy_notification" class="hidden mt-1 text-xs text-green-600">
                                            Password copied to clipboard!
                                        </div>
                                    </div>
                                    
                                    <div>
                                        <label for="password" class="block text-sm font-medium text-gray-700">
                                            New Password (leave blank to keep current)
                                        </label>
                                        <div class="mt-1 relative">
                                            <input type="password" name="password" id="password"
                                                   placeholder="Enter new password to change"
                                                   class="focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md pr-10">
                                            <button type="button"
                                                    onclick="togglePasswordVisibility('password', 'eye_icon_new')"
                                                    class="absolute inset-y-0 right-0 pr-3 flex items-center">
                                                <svg id="eye_icon_new" class="h-5 w-5 text-gray-400 hover:text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <!-- Eye closed icon (default) -->
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                                                </svg>
                                            </button>
                                        </div>
                                    </div>
                                    
                                    <div>
                                        <label for="password_updated_at" class="block text-sm font-medium text-gray-700">
                                            Password Last Updated Date
                                        </label>
                                        <input type="date" name="password_updated_at" id="password_updated_at"
                                               value="{password_updated_at.strftime("%Y-%m-%d") if password_updated_at else ""}"
                                               class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                                        <p class="mt-1 text-xs text-gray-500">
                                            Use this to adjust when the password was last updated.
                                        </p>
                                    </div>
                                    
                                    <div>
                                        <label for="current_expiry" class="block text-sm font-medium text-gray-700">
                                            Current Expiry Date
                                        </label>
                                        <input type="text" id="current_expiry" 
                                               value="{password_expires_at.strftime('%Y-%m-%d') if password_expires_at else 'Not set'}"
                                               class="mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md bg-gray-100"
                                               disabled>
                                        <p class="mt-1 text-xs text-gray-500">
                                            {f'{days_left} days remaining' if days_left is not None else 'No expiry tracking'}
                                        </p>
                                    </div>
                                    
                                    <div>
                                        <label for="expires_days" class="block text-sm font-medium text-gray-700">
                                            Password Expiry Period (days)
                                        </label>
                                        <input type="number" name="expires_days" id="expires_days" 
                                               value="{expiry_period}"
                                               min="0"
                                               class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                               onchange="updateExpiryPreview()">
                                        <p class="mt-1 text-xs text-gray-500">
                                            Days until expiry from the update date (0 to disable)
                                        </p>
                                        <p id="expiry-preview" class="mt-1 text-xs text-blue-600"></p>
                                    </div>
                                </div>
                                
                                <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                                    <button type="submit"
                                            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:col-start-2 sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed">
                                        Update
                                    </button>
                                    <button type="button" 
                                            onclick="document.getElementById('modal').innerHTML=''"
                                            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:col-start-1 sm:text-sm">
                                        Cancel
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <script>
            // Enable HTMX debugging
            if (typeof htmx !== 'undefined') {{
                htmx.logAll();
                console.log('HTMX version:', htmx.version);
                // Process the form to ensure HTMX is aware of it
                htmx.process(document.querySelector('form[hx-put]'));
            }} else {{
                console.error('HTMX is not loaded!');
            }}
            
            // Function to toggle password visibility
            function togglePasswordVisibility(inputId, iconId) {{
                const input = document.getElementById(inputId);
                const icon = document.getElementById(iconId);
                
                if (input.type === 'password') {{
                    input.type = 'text';
                    // Change to eye open icon
                    icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />';
                    icon.classList.remove('text-gray-400');
                    icon.classList.add('text-indigo-600');
                }} else {{
                    input.type = 'password';
                    // Change back to eye closed icon
                    icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />';
                    icon.classList.remove('text-indigo-600');
                    icon.classList.add('text-gray-400');
                }}
            }}
            
            // Function to copy password to clipboard
            function copyPassword(inputId) {{
                const input = document.getElementById(inputId);
                const notification = document.getElementById('copy_notification');
                
                // Temporarily change type to text if needed
                const wasPassword = input.type === 'password';
                if (wasPassword) {{
                    input.type = 'text';
                }}
                
                // Select and copy
                input.select();
                input.setSelectionRange(0, 99999); // For mobile devices
                
                try {{
                    document.execCommand('copy');
                    // Show notification
                    notification.classList.remove('hidden');
                    setTimeout(() => {{
                        notification.classList.add('hidden');
                    }}, 3000);
                }} catch (err) {{
                    console.error('Failed to copy password:', err);
                    alert('Failed to copy password. Please select and copy manually.');
                }}
                
                // Restore password type if needed
                if (wasPassword) {{
                    input.type = 'password';
                }}
                
                // Remove selection
                input.blur();
            }}
            
            // Function to update expiry preview
            function updateExpiryPreview() {{
                const updateDateInput = document.getElementById('password_updated_at');
                const expireDaysInput = document.getElementById('expires_days');
                const preview = document.getElementById('expiry-preview');
                
                const updateDate = updateDateInput.value;
                const expireDays = parseInt(expireDaysInput.value) || 0;
                
                if (updateDate && expireDays > 0) {{
                    const date = new Date(updateDate + 'T00:00:00Z');
                    date.setDate(date.getDate() + expireDays);
                    
                    const expiryDate = date.toLocaleDateString('en-US', {{
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                    }});
                    
                    // Calculate days from today
                    const today = new Date();
                    today.setHours(0, 0, 0, 0);
                    const daysUntilExpiry = Math.floor((date - today) / (1000 * 60 * 60 * 24));
                    
                    let message = `New expiry date will be: ${{expiryDate}}`;
                    let className = 'text-blue-600';
                    
                    if (daysUntilExpiry < 0) {{
                        message += ` (expired ${{Math.abs(daysUntilExpiry)}} days ago)`;
                        className = 'text-red-600';
                    }} else if (daysUntilExpiry === 0) {{
                        message += ` (expires today!)`;
                        className = 'text-red-600 font-medium';
                    }} else if (daysUntilExpiry <= 7) {{
                        message += ` (in ${{daysUntilExpiry}} days)`;
                        className = 'text-red-600';
                    }} else if (daysUntilExpiry <= 30) {{
                        message += ` (in ${{daysUntilExpiry}} days)`;
                        className = 'text-yellow-600';
                    }} else {{
                        message += ` (in ${{daysUntilExpiry}} days)`;
                        className = 'text-green-600';
                    }}
                    
                    preview.className = `mt-1 text-xs ${{className}}`;
                    preview.textContent = message;
                }} else if (expireDays === 0) {{
                    preview.className = 'mt-1 text-xs text-gray-600';
                    preview.textContent = 'Password expiry tracking will be disabled';
                }} else {{
                    preview.textContent = '';
                }}
            }}
            
            // Add event listeners
            document.getElementById('password_updated_at').addEventListener('change', updateExpiryPreview);
            document.getElementById('expires_days').addEventListener('input', updateExpiryPreview);
            
            // Initial calculation
            updateExpiryPreview();
        </script>
        """

        return HTMLResponse(content=html)
    except Exception as e:
        return HTMLResponse(
            content=f'<div class="text-red-600 p-4">Error: {str(e)}</div>',
            status_code=500,
        )


# Updated update_environment function for dbcreds/web/main.py


@app.put("/environments/{env_name}", response_class=HTMLResponse)
async def update_environment(request: Request, env_name: str):
    """Update an environment."""
    try:
        form_data = await request.form()
        # Never log sensitive form data - create sanitized version for logging
        safe_form_data = dict(form_data)
        if 'password' in safe_form_data:
            safe_form_data['password'] = '***REDACTED***'
        logger.info(f"Updating environment {env_name} with form data keys: {list(form_data.keys())}")
        manager = CredentialManager()

        # Get existing credentials
        creds = manager.get_credentials(env_name, check_expiry=False)

        # Get the expires_days value
        expires_days = int(form_data.get("expires_days", 90))
        
        # Calculate current expiry period if it exists
        current_expiry_days = 90  # Default
        if creds.password_expires_at and creds.password_updated_at:
            delta = creds.password_expires_at - creds.password_updated_at
            current_expiry_days = delta.days
        
        logger.debug(f"Current state for {env_name}: updated_at={creds.password_updated_at}, expires_at={creds.password_expires_at}, current_expiry_days={current_expiry_days}")

        # Check if password updated date was changed
        new_update_date_str = form_data.get("password_updated_at", "").strip()
        form_provided_date = None  # Track if date was explicitly provided in form
        if new_update_date_str:
            # Parse the date from the form
            try:
                # Parse as naive datetime then make timezone aware
                naive_dt = datetime.strptime(new_update_date_str, "%Y-%m-%d")
                form_provided_date = naive_dt.replace(tzinfo=timezone.utc)
            except ValueError:
                return HTMLResponse(
                    content='<div class="text-red-600 p-4">Error: Invalid date format</div>',
                    status_code=400,
                )

        # Update password or other fields if needed
        new_password = form_data.get("password", "").strip()
        old_password = creds.password.get_secret_value()
        logger.info(f"Password update check: new_provided={bool(new_password)}, new_length={len(new_password) if new_password else 0}, old_length={len(old_password)}")
        
        # Determine what date to use
        # Priority: 1. Form-provided date, 2. Existing date (if no form date)
        if form_provided_date:
            password_updated_at = form_provided_date
            date_changed = (password_updated_at != creds.password_updated_at)
            logger.debug(f"Using form-provided date: {password_updated_at}, changed from: {creds.password_updated_at}")
        else:
            # No date in form, use existing
            password_updated_at = creds.password_updated_at
            date_changed = False
            # Ensure it's timezone aware
            if password_updated_at and password_updated_at.tzinfo is None:
                password_updated_at = password_updated_at.replace(tzinfo=timezone.utc)
            logger.debug(f"No date in form, using existing: {password_updated_at}")

        # If there's no password_expires_at but we have updated_at and expires_days,
        # we should update to add the expiry
        needs_expiry_fix = (
            creds.password_expires_at is None
            and password_updated_at
            and expires_days > 0
        )
        
        # Check if expiry period actually changed
        expiry_changed = (expires_days != current_expiry_days)

        # Determine if we need to update
        update_needed = (
            new_password or          # Password changed
            date_changed or           # Date explicitly changed
            expiry_changed or         # Expiry period changed
            needs_expiry_fix          # Need to fix missing expiry
        )

        if update_needed:
            # We need to update the credentials
            if not new_password:
                # If only changing the update date or expiry, reuse existing password
                new_password = creds.password.get_secret_value()
                logger.debug(f"No new password provided, using existing password")
            else:
                logger.info(f"New password provided, will update password")

            logger.info(f"Calling set_credentials with password_length={len(new_password)}, updated_at={password_updated_at}")
            
            # Set credentials with the custom password_updated_at timestamp
            manager.set_credentials(
                env_name,
                host=creds.host,
                port=creds.port,
                database=creds.database,
                username=creds.username,
                password=new_password,
                password_expires_days=expires_days if expires_days > 0 else None,
                password_updated_at=password_updated_at,  # Pass the custom timestamp
            )

            # Log what we did
            logger.info(
                f"Updated environment {env_name}: password_changed={bool(form_data.get('password'))}, "
                f"date_changed={date_changed}, "
                f"expiry_days={expires_days}, "
                f"password_updated_at={password_updated_at.isoformat() if password_updated_at else 'None'}"
            )
            
            # Verify the update by immediately retrieving
            verify_creds = manager.get_credentials(env_name, check_expiry=False)
            logger.info(f"Verification after update: password_matches_new={verify_creds.password.get_secret_value() == new_password}, password_length={len(verify_creds.password.get_secret_value())}")

        # Get updated environments list
        environments = manager.list_environments()

        # Return response with environment list and trigger events
        return HTMLResponse(
            content=f"""
            <div id="environment-list" hx-swap-oob="true">
                {
                templates.get_template("partials/environment_list.html").render(
                    request=request, environments=environments
                )
            }
            </div>
            <div id="modal" hx-swap-oob="true"></div>
            <div id="notification-container" hx-swap-oob="afterbegin">
                <div class="fixed top-4 right-4 z-50 animate-fade-in-down">
                    <div class="bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded-lg shadow-lg flex items-center space-x-3">
                        <svg class="h-5 w-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                        </svg>
                        <span class="font-medium">Environment '{
                env_name
            }' updated successfully!</span>
                    </div>
                </div>
                <script>
                    // Remove notification after 3 seconds
                    setTimeout(() => {{
                        const notification = document.querySelector('#notification-container > div');
                        if (notification) {{
                            notification.classList.add('animate-fade-out-up');
                            setTimeout(() => notification.remove(), 300);
                        }}
                    }}, 3000);
                    
                    // Reload expiry info for the updated environment
                    setTimeout(() => loadExpiryInfo('{env_name}'), 100);
                </script>
            </div>
            """
        )
    except Exception as e:
        logger.error(f"Error updating environment {env_name}: {e}")
        return HTMLResponse(
            content=f"""
            <div class="text-red-600 p-4">Error: {str(e)}</div>
            <div id="notification-container" hx-swap-oob="afterbegin">
                <div class="fixed top-4 right-4 z-50 animate-fade-in-down">
                    <div class="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg shadow-lg flex items-center space-x-3">
                        <svg class="h-5 w-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                        <span class="font-medium">Error updating environment: {str(e)}</span>
                    </div>
                </div>
                <script>
                    // Remove notification after 5 seconds
                    setTimeout(() => {{
                        const notification = document.querySelector('#notification-container > div');
                        if (notification) {{
                            notification.classList.add('animate-fade-out-up');
                            setTimeout(() => notification.remove(), 300);
                        }}
                    }}, 5000);
                </script>
            </div>
            """,
            status_code=400,
        )


@app.post("/environments/{env_name}/test", response_class=HTMLResponse)
async def test_environment(request: Request, env_name: str):
    """Test environment connection."""
    try:
        manager = CredentialManager()
        success = manager.test_connection(env_name)

        if success:
            return HTMLResponse(
                content='<div class="text-green-600 p-4">✓ Connection successful!</div>'
            )
        else:
            return HTMLResponse(
                content='<div class="text-red-600 p-4">✗ Connection failed!</div>'
            )
    except Exception as e:
        return HTMLResponse(
            content=f'<div class="text-red-600 p-4">Error: {str(e)}</div>',
            status_code=500,
        )


@app.get("/environments/new", response_class=HTMLResponse)
async def new_environment_form(request: Request):
    """New environment form (HTMX modal)."""
    # Default ports for each database type
    default_ports = {
        DatabaseType.POSTGRESQL: 5432,
        DatabaseType.MYSQL: 3306,
        DatabaseType.MSSQL: 1433,
        DatabaseType.ORACLE: 1521,
    }

    # Get today's date for the default
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    return HTMLResponse(
        content=f"""
    <div class="fixed z-10 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
            <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
            <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
                <div>
                    <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                        Add New Environment
                    </h3>
                    <div class="mt-2">
                        <form hx-post="/environments" 
                              hx-target="#environment-list" 
                              hx-swap="innerHTML"
                              hx-indicator="#form-indicator">
                            <!-- Loading indicator -->
                            <div id="form-indicator" class="htmx-indicator fixed inset-0 bg-gray-500 bg-opacity-50 flex items-center justify-center rounded-lg" style="display:none;">
                                <div class="bg-white p-4 rounded-lg shadow-lg flex items-center space-x-3">
                                    <svg class="animate-spin h-5 w-5 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    <span class="text-gray-700">Creating environment...</span>
                                </div>
                            </div>
                            
                            <div class="space-y-4 max-h-[60vh] overflow-y-auto pr-2">
                                <div>
                                    <label for="name" class="block text-sm font-medium text-gray-700">
                                        Environment Name
                                    </label>
                                    <input type="text" name="name" id="name" required
                                           class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                           placeholder="dev, staging, prod">
                                </div>
                                
                                <div>
                                    <label for="database_type" class="block text-sm font-medium text-gray-700">
                                        Database Type
                                    </label>
                                    <select name="database_type" id="database_type" required
                                            class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                                            onchange="updateDefaultPort(this.value)">
                                        {"".join(f'<option value="{dt.value}" data-port="{default_ports.get(dt, 5432)}">{dt.value.title()}</option>' for dt in DatabaseType)}
                                    </select>
                                </div>
                                
                                <div class="grid grid-cols-2 gap-4">
                                    <div>
                                        <label for="host" class="block text-sm font-medium text-gray-700">
                                            Server/Host
                                        </label>
                                        <input type="text" name="host" id="host" required
                                               class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                               placeholder="localhost">
                                    </div>
                                    
                                    <div>
                                        <label for="port" class="block text-sm font-medium text-gray-700">
                                            Port
                                        </label>
                                        <input type="number" name="port" id="port" required value="5432"
                                               class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                                    </div>
                                </div>
                                
                                <div>
                                    <label for="database" class="block text-sm font-medium text-gray-700">
                                        Database Name
                                    </label>
                                    <input type="text" name="database" id="database" required
                                           class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                           placeholder="mydb">
                                </div>
                                
                                <div>
                                    <label for="username" class="block text-sm font-medium text-gray-700">
                                        Username
                                    </label>
                                    <input type="text" name="username" id="username" required
                                           class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                                </div>
                                
                                <div>
                                    <label for="password" class="block text-sm font-medium text-gray-700">
                                        Password
                                    </label>
                                    <input type="password" name="password" id="password" required
                                           class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                                </div>
                                
                                <!-- Separator line for password management section -->
                                <div class="border-t border-gray-200 pt-4">
                                    <h4 class="text-sm font-medium text-gray-700 mb-3">Password Management</h4>
                                    
                                    <div>
                                        <label for="password_updated_at" class="block text-sm font-medium text-gray-700">
                                            Password Last Updated Date
                                        </label>
                                        <input type="date" name="password_updated_at" id="password_updated_at"
                                               value="{today}"
                                               max="{today}"
                                               class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                               onchange="updateExpiryPreview()">
                                        <p class="mt-1 text-xs text-gray-500">
                                            When was this password last set or changed? Defaults to today.
                                        </p>
                                    </div>
                                    
                                    <div class="mt-4">
                                        <label for="expires_days" class="block text-sm font-medium text-gray-700">
                                            Password Expiry Period (days)
                                        </label>
                                        <input type="number" name="expires_days" id="expires_days" value="90" min="0"
                                               class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                               oninput="updateExpiryPreview()">
                                        <p class="mt-1 text-xs text-gray-500">
                                            How many days until the password expires from the update date. Set to 0 to disable expiry.
                                        </p>
                                        <p id="expiry-preview" class="mt-1 text-xs"></p>
                                    </div>
                                </div>
                                
                                <div>
                                    <label for="description" class="block text-sm font-medium text-gray-700">
                                        Description
                                    </label>
                                    <input type="text" name="description" id="description"
                                           class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                           placeholder="Optional description">
                                </div>
                                
                                <div class="flex items-center">
                                    <input type="checkbox" name="is_production" id="is_production"
                                           class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded">
                                    <label for="is_production" class="ml-2 block text-sm text-gray-900">
                                        Production Environment
                                    </label>
                                </div>
                            </div>
                            
                            <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                                <button type="submit"
                                        class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:col-start-2 sm:text-sm">
                                    Add Environment
                                </button>
                                <button type="button" onclick="document.getElementById('modal').innerHTML=''"
                                        class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:col-start-1 sm:text-sm">
                                    Cancel
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script>
        function updateDefaultPort(dbType) {{
            const select = document.getElementById('database_type');
            const option = select.querySelector(`option[value="${{dbType}}"]`);
            const port = option.getAttribute('data-port');
            document.getElementById('port').value = port;
        }}
        
        function updateExpiryPreview() {{
            const updateDateInput = document.getElementById('password_updated_at');
            const expireDaysInput = document.getElementById('expires_days');
            
            const updateDate = updateDateInput.value;
            const expireDays = parseInt(expireDaysInput.value) || 0;
            
            if (updateDate && expireDays > 0) {{
                const date = new Date(updateDate + 'T00:00:00Z');
                date.setDate(date.getDate() + expireDays);
                
                const expiryDate = date.toLocaleDateString('en-US', {{
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                }});
                
                // Check if already expired
                const today = new Date();
                today.setHours(0, 0, 0, 0);
                
                const daysUntilExpiry = Math.floor((date - today) / (1000 * 60 * 60 * 24));
                
                let message = `Password will expire on ${{expiryDate}}`;
                let className = 'text-gray-600';
                
                if (daysUntilExpiry < 0) {{
                    message = `Password would have expired on ${{expiryDate}} (${{Math.abs(daysUntilExpiry)}} days ago)`;
                    className = 'text-red-600';
                }} else if (daysUntilExpiry === 0) {{
                    message = `Password expires today!`;
                    className = 'text-red-600 font-medium';
                }} else if (daysUntilExpiry <= 7) {{
                    message = `Password will expire on ${{expiryDate}} (in ${{daysUntilExpiry}} days)`;
                    className = 'text-red-600';
                }} else if (daysUntilExpiry <= 30) {{
                    message = `Password will expire on ${{expiryDate}} (in ${{daysUntilExpiry}} days)`;
                    className = 'text-yellow-600';
                }} else {{
                    message = `Password will expire on ${{expiryDate}} (in ${{daysUntilExpiry}} days)`;
                    className = 'text-green-600';
                }}
                
                // Update preview
                const preview = document.getElementById('expiry-preview');
                preview.className = `mt-1 text-xs ${{className}}`;
                preview.textContent = message;
            }} else if (expireDays === 0) {{
                const preview = document.getElementById('expiry-preview');
                preview.className = 'mt-1 text-xs text-blue-600';
                preview.textContent = 'Password expiry tracking disabled';
            }} else {{
                // Clear preview
                const preview = document.getElementById('expiry-preview');
                preview.textContent = '';
            }}
        }}
        
        // Initial calculation
        updateExpiryPreview();
    </script>
    """
    )


@app.get("/api/environments/{env_name}/expiry")
async def get_environment_expiry(env_name: str):
    """Get password expiry information for an environment."""
    try:
        manager = CredentialManager()
        creds = manager.get_credentials(env_name, check_expiry=False)

        # Helper function to ensure datetime is timezone-aware
        def ensure_timezone_aware(dt):
            if dt and dt.tzinfo is None:
                # If naive, assume it was UTC
                return dt.replace(tzinfo=timezone.utc)
            return dt

        # Calculate days until expiry
        days_left = None
        expiry_days = 90  # Default value

        # Ensure all datetimes are timezone-aware
        password_updated_at = ensure_timezone_aware(creds.password_updated_at)
        password_expires_at = ensure_timezone_aware(creds.password_expires_at)

        if password_expires_at and password_updated_at:
            # We have both dates - calculate actual values
            expiry_days = (password_expires_at - password_updated_at).days
            # Calculate days left until expiry
            now_utc = datetime.now(timezone.utc)
            delta = password_expires_at - now_utc
            days_left = max(0, delta.days)  # Use max to avoid negative days
        elif password_updated_at:
            # We have updated_at but no expires_at
            # This means expiry is not being tracked, but we can calculate theoretical expiry
            # Don't set days_left here - let the frontend calculate it if needed
            pass

        # Check if expired
        is_expired = False
        if password_expires_at:
            is_expired = datetime.now(timezone.utc) > password_expires_at

        return {
            "days_left": days_left,
            "is_expired": is_expired,
            "expires_at": password_expires_at.isoformat()
            if password_expires_at
            else None,
            "updated_at": password_updated_at.isoformat()
            if password_updated_at
            else None,
            "has_expiry": password_expires_at
            is not None,  # Only true if actually tracking expiry
            "expires_days": expiry_days,  # Always return this so frontend can calculate
        }
    except Exception as e:
        logger.error(f"Error getting expiry for {env_name}: {e}")
        import traceback

        logger.error(traceback.format_exc())
        return {
            "error": str(e),
            "days_left": None,
            "is_expired": False,
            "updated_at": None,
            "has_expiry": False,
            "expires_days": 90,  # Default
        }


def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """Run the web server."""
    # Show security warnings in development
    if not os.getenv("DBCREDS_PRODUCTION", "").lower() == "true":
        print_security_warnings()
    
    console.print("\n[bold blue]Starting dbcreds web server[/bold blue]")
    console.print(f"[green]➜[/green] Local:   http://localhost:{port}")
    console.print(f"[green]➜[/green] Network: http://{host}:{port}\n")

    # Configure uvicorn with custom logging
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["default"]["fmt"] = "%(levelprefix)s %(message)s"
    log_config["formatters"]["access"]["fmt"] = (
        '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
    )

    uvicorn.run(
        "dbcreds.web.main:app" if reload else app,
        host=host,
        port=port,
        reload=reload,
        log_config=log_config,
    )


if __name__ == "__main__":
    run_server(reload=True)
