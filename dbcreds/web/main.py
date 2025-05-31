# dbcreds/web/main.py
"""
FastAPI web application for dbcreds.

Provides a web interface for managing database credentials with
team collaboration features.
"""

import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
from rich.console import Console
from rich.panel import Panel  # Add this import
from rich.traceback import install as install_rich_traceback

from dbcreds import __version__
from dbcreds.core.exceptions import CredentialError
from dbcreds.core.manager import CredentialManager
from dbcreds.web.errors import web_error_handler
from datetime import datetime
from dbcreds.core.models import DatabaseType
import json
# Install rich traceback handler
install_rich_traceback(show_locals=True)

# Create console for startup messages
console = Console()

# Create FastAPI app
app = FastAPI(
    title="dbcreds Web",
    description="Database Credentials Management",
    version=__version__,
)

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


@app.on_event("startup")
async def startup_event():
    """Run on startup."""
    console.print(Panel.fit(
        f"[bold green]dbcreds Web Server v{__version__}[/bold green]\n"
        f"[dim]Ready to manage your database credentials[/dim]",
        title="Starting Up",
        border_style="green"
    ))


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
        # Errors will be caught by exception handlers
        raise


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
            status_code=500
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
                "available": backend.is_available()
            }
            
            # Add descriptions for known backends
            if "Keyring" in backend_name:
                backend_info["description"] = "System keyring (Keychain on macOS, Credential Manager on Windows)"
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
    except Exception as e:
        # Errors will be caught by exception handlers
        raise


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
            is_production=bool(form_data.get("is_production", False))
        )
        
        # Set credentials
        manager.set_credentials(
            env_name,
            host=form_data.get("host"),
            port=int(form_data.get("port", 5432)),
            database=form_data.get("database"),
            username=form_data.get("username"),
            password=form_data.get("password"),
            password_expires_days=int(form_data.get("expires_days", 90))
        )
        
        # Return updated environment list
        environments = manager.list_environments()
        return templates.TemplateResponse(
            "partials/environment_list.html",
            {"request": request, "environments": environments},
        )
    except Exception as e:
        return HTMLResponse(
            content=f'<div class="text-red-600 p-4">Error: {str(e)}</div>',
            status_code=400
        )


@app.get("/environments/{env_name}/edit", response_class=HTMLResponse)
async def edit_environment_form(request: Request, env_name: str):
    """Get edit form for an environment."""
    try:
        manager = CredentialManager()
        creds = manager.get_credentials(env_name, check_expiry=False)
        env = next((e for e in manager.list_environments() if e.name == env_name), None)
        
        if not env:
            raise HTTPException(status_code=404, detail="Environment not found")
        
        # Calculate days until expiry
        days_left = creds.days_until_expiry()
        
        # Calculate the total expiry period (not the days left)
        expiry_period = 90  # Default
        if creds.password_expires_at and creds.password_updated_at:
            expiry_period = (creds.password_expires_at - creds.password_updated_at).days
        
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
                            <form hx-put="/environments/{env_name}" hx-target="#environment-list" hx-swap="innerHTML">
                                <div class="space-y-4">
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700">
                                            Connection Details
                                        </label>
                                        <div class="mt-1 text-sm text-gray-500">
                                            Host: {creds.host}:{creds.port}<br>
                                            Database: {creds.database}<br>
                                            Username: {creds.username}<br>
                                            Type: {env.database_type.value}
                                        </div>
                                    </div>
                                    
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700">
                                            Password Status
                                        </label>
                                        <div class="mt-1 text-sm">
                                            {'''
                                            <span class="text-red-600">Expired</span>
                                            ''' if creds.is_password_expired() else f'''
                                            <span class="text-green-600">{days_left} days remaining</span>
                                            ''' if days_left is not None else '''
                                            <span class="text-gray-600">No expiry set</span>
                                            '''}
                                            <div class="text-xs text-gray-500 mt-1">
                                                Last updated: {creds.password_updated_at.strftime('%Y-%m-%d')}
                                                {f'''<br>Expires on: {creds.password_expires_at.strftime('%Y-%m-%d')}''' if creds.password_expires_at else ''}
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div>
                                        <label for="password" class="block text-sm font-medium text-gray-700">
                                            New Password (leave blank to keep current)
                                        </label>
                                        <input type="password" name="password" id="password"
                                               class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                                    </div>
                                    
                                    <div>
                                        <label for="password_updated_at" class="block text-sm font-medium text-gray-700">
                                            Password Last Updated Date
                                        </label>
                                        <input type="date" name="password_updated_at" id="password_updated_at"
                                               value="{creds.password_updated_at.strftime('%Y-%m-%d')}"
                                               class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                                        <p class="mt-1 text-xs text-gray-500">
                                            Use this to adjust when the password was last updated.
                                        </p>
                                    </div>
                                    
                                    <div>
                                        <label for="expires_days" class="block text-sm font-medium text-gray-700">
                                            Password Expiry (days)
                                        </label>
                                        <input type="number" name="expires_days" id="expires_days" 
                                               value="{expiry_period}"
                                               class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                                        <p class="mt-1 text-xs text-gray-500">
                                            Total days passwords are valid for (from update date).
                                        </p>
                                    </div>
                                </div>
                                
                                <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                                    <button type="submit"
                                            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:col-start-2 sm:text-sm">
                                        Update
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
        """
        
        return HTMLResponse(content=html)
    except Exception as e:
        return HTMLResponse(
            content=f'<div class="text-red-600 p-4">Error: {str(e)}</div>',
            status_code=500
        )

@app.put("/environments/{env_name}", response_class=HTMLResponse)
async def update_environment(request: Request, env_name: str):
    """Update an environment."""
    try:
        form_data = await request.form()
        manager = CredentialManager()
        
        # Get existing credentials
        creds = manager.get_credentials(env_name, check_expiry=False)
        
        # Get the expires_days value
        expires_days = int(form_data.get("expires_days", 90))
        
        # Check if password updated date was changed
        new_update_date_str = form_data.get("password_updated_at", "").strip()
        password_updated_at = None
        if new_update_date_str:
            from datetime import datetime
            # Parse the date from the form
            try:
                password_updated_at = datetime.strptime(new_update_date_str, '%Y-%m-%d')
            except ValueError:
                return HTMLResponse(
                    content='<div class="text-red-600 p-4">Error: Invalid date format</div>',
                    status_code=400
                )
        
        # Update password or other fields if needed
        new_password = form_data.get("password", "").strip()
        # Always consider an update needed if expiry days are set
        update_needed = new_password or password_updated_at or expires_days > 0
        
        if update_needed:
            # We need to directly modify the credentials in the backend
            if not new_password:
                # If only changing the update date, reuse existing password
                new_password = creds.password.get_secret_value()
                
            # Use the existing update date if not provided
            if not password_updated_at:
                password_updated_at = creds.password_updated_at
            
            # Create a new credentials object with updated fields
            manager.set_credentials(
                env_name,
                host=creds.host,
                port=creds.port,
                database=creds.database,
                username=creds.username,
                password=new_password,
                # Always set the password_expires_days to ensure expiry is calculated
                password_expires_days=expires_days
            )
            
            # If we need to modify the update date, we need to access the backends
            if password_updated_at:
                # We need to update the password_updated_at field directly
                for backend in manager.backends:
                    if backend.is_available():
                        try:
                            # Get the raw credentials from the backend
                            result = backend.get_credential(f"dbcreds:{env_name}")
                            if result:
                                username, password, metadata = result
                                # Modify the password_updated_at field in metadata
                                metadata["password_updated_at"] = password_updated_at.isoformat()
                                # Always calculate the new expiry date
                                from datetime import timedelta
                                expires_at = password_updated_at + timedelta(days=expires_days)
                                metadata["password_expires_at"] = expires_at.isoformat()
                                # Save back to the backend using set_credential
                                backend.set_credential(f"dbcreds:{env_name}", username, password, metadata)
                                break
                        except Exception as backend_error:
                            logger.error(f"Error updating credentials in backend {backend.__class__.__name__}: {backend_error}")
                            continue
        
        # Clear modal and refresh list
        environments = manager.list_environments()
        return templates.TemplateResponse(
            "partials/environment_list.html",
            {"request": request, "environments": environments},
        )
    except Exception as e:
        return HTMLResponse(
            content=f'<div class="text-red-600 p-4">Error: {str(e)}</div>',
            status_code=400
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
            status_code=500
        )


@app.get("/environments/new", response_class=HTMLResponse)
async def new_environment_form(request: Request):
    """New environment form (HTMX modal)."""
    from dbcreds.core.models import DatabaseType
    
    # Default ports for each database type
    default_ports = {
        DatabaseType.POSTGRESQL: 5432,
        DatabaseType.MYSQL: 3306,
        DatabaseType.MSSQL: 1433,
        DatabaseType.ORACLE: 1521,
    }
    
    return HTMLResponse(content=f"""
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
                        <form hx-post="/environments" hx-target="#environment-list" hx-swap="innerHTML">
                            <div class="space-y-4">
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
                                        {''.join(f'<option value="{dt.value}" data-port="{default_ports.get(dt, 5432)}">{dt.value.title()}</option>' for dt in DatabaseType)}
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
                                
                                <div>
                                    <label for="expires_days" class="block text-sm font-medium text-gray-700">
                                        Password Expiry (days)
                                    </label>
                                    <input type="number" name="expires_days" id="expires_days" value="90"
                                           class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
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
    </script>
    """)
@app.get("/api/environments/{env_name}/expiry")
async def get_environment_expiry(env_name: str):
    """Get password expiry information for an environment."""
    try:
        manager = CredentialManager()
        creds = manager.get_credentials(env_name, check_expiry=False)
        
        # Calculate days until expiry
        days_left = None
        expiry_days = 90  # Default value
        
        if creds.password_expires_at and creds.password_updated_at:
            # Calculate the total expiry period in days
            expiry_days = (creds.password_expires_at - creds.password_updated_at).days
            days_left = creds.days_until_expiry()
        elif creds.password_updated_at:
            # If we have updated_at but no expires_at, calculate it with default 90 days
            from datetime import timedelta, datetime
            expires_at = creds.password_updated_at + timedelta(days=expiry_days)
            delta = expires_at - datetime.utcnow()
            days_left = delta.days if delta.days > 0 else 0
        
        return {
            "days_left": days_left,
            "is_expired": creds.is_password_expired() if creds.password_expires_at else (days_left == 0 if days_left is not None else False),
            "expires_at": creds.password_expires_at.isoformat() if creds.password_expires_at else None,
            "updated_at": creds.password_updated_at.isoformat() if creds.password_updated_at else None,
            "has_expiry": creds.password_expires_at is not None or creds.password_updated_at is not None,
            "expires_days": expiry_days  # Total expiry window
        }
    except Exception as e:
        logger.error(f"Error getting expiry for {env_name}: {e}")
        return {"error": str(e), "days_left": None, "is_expired": False, "updated_at": None, "has_expiry": False}



def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """Run the web server."""
    console.print(f"\n[bold blue]Starting dbcreds web server[/bold blue]")
    console.print(f"[green]➜[/green] Local:   http://localhost:{port}")
    console.print(f"[green]➜[/green] Network: http://{host}:{port}\n")
    
    # Configure uvicorn with custom logging
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["default"]["fmt"] = "%(levelprefix)s %(message)s"
    log_config["formatters"]["access"]["fmt"] = '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
    
    uvicorn.run(
        "dbcreds.web.main:app" if reload else app,
        host=host,
        port=port,
        reload=reload,
        log_config=log_config,
    )


if __name__ == "__main__":
    run_server(reload=True)