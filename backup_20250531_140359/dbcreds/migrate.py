# dbcreds/migrate.py
"""
Migration script for importing existing PowerShell credentials into dbcreds.
"""

import os
import sys
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

from dbcreds.core.manager import CredentialManager
from dbcreds.core.models import DatabaseType

console = Console()


def detect_database_type(port: int, server: str = "") -> DatabaseType:
    """Detect database type from port or server name."""
    port_mapping = {
        5432: DatabaseType.POSTGRESQL,
        3306: DatabaseType.MYSQL,
        1433: DatabaseType.MSSQL,
        1521: DatabaseType.ORACLE,
    }
    
    # Check port first
    if port in port_mapping:
        return port_mapping[port]
    
    # Check server name for hints
    server_lower = server.lower()
    if "postgres" in server_lower or "pg" in server_lower or "rds" in server_lower:
        return DatabaseType.POSTGRESQL
    elif "mysql" in server_lower or "maria" in server_lower:
        return DatabaseType.MYSQL
    elif "mssql" in server_lower or "sqlserver" in server_lower:
        return DatabaseType.MSSQL
    elif "oracle" in server_lower:
        return DatabaseType.ORACLE
    
    # Default to PostgreSQL
    return DatabaseType.POSTGRESQL


def main(
    env_name: str = typer.Option("default", "--name", "-n", help="Environment name for dbcreds"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite if exists"),
):
    """Import credentials from PowerShell environment variables."""
    console.print("[bold blue]Importing credentials from PowerShell environment...[/bold blue]")
    
    # Check for required environment variables
    required_vars = ["DB_SERVER", "DB_PORT", "DB_NAME", "DB_USER"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        console.print(f"[red]Missing environment variables: {', '.join(missing_vars)}[/red]")
        console.print("[yellow]Please run your PowerShell profile first to set up the environment.[/yellow]")
        console.print("\nTry running these commands first:")
        console.print("  Connect-ODS")
        console.print("  # or")
        console.print("  update-db")
        sys.exit(1)
    
    # Get values from environment
    server = os.environ.get("DB_SERVER")
    port = int(os.environ.get("DB_PORT", 5432))
    database = os.environ.get("DB_NAME")
    username = os.environ.get("DB_USER")
    password = os.environ.get("DB_PWD")
    
    # Try to get password from Windows Credential Manager if not in env
    if not password:
        try:
            from dbcreds.backends.legacy_windows import LegacyWindowsBackend
            backend = LegacyWindowsBackend()
            legacy_target = f"DBCredentials:{database}"
            password = backend._get_password_from_legacy_target(legacy_target)
            if password:
                console.print("[green]Retrieved password from Windows Credential Manager[/green]")
        except Exception as e:
            console.print(f"[yellow]Could not retrieve password from Credential Manager: {e}[/yellow]")
    
    if not password:
        console.print("[red]No password found in environment or Credential Manager![/red]")
        console.print("\nMake sure you have run one of these commands:")
        console.print("  update-db")
        console.print("  Set-DatabaseEnvironment")
        sys.exit(1)
    
    # Detect database type
    db_type = detect_database_type(port, server)
    
    # Show what will be imported
    panel = Panel(
        f"""[cyan]Server:[/cyan] {server}
[cyan]Port:[/cyan] {port}
[cyan]Database:[/cyan] {database}
[cyan]Username:[/cyan] {username}
[cyan]Password:[/cyan] ********
[cyan]Type:[/cyan] {db_type.value}
[cyan]Environment:[/cyan] {env_name}""",
        title="Credentials to Import",
        border_style="green",
    )
    console.print(panel)
    
    # Confirm import
    if not Confirm.ask("Import these credentials?"):
        console.print("[yellow]Import cancelled.[/yellow]")
        return
    
    # Import into dbcreds
    manager = CredentialManager()
    
    try:
        # Check if environment exists
        existing_envs = [env.name for env in manager.list_environments()]
        if env_name in existing_envs:
            if not force:
                console.print(f"[yellow]Environment '{env_name}' already exists![/yellow]")
                if not Confirm.ask("Overwrite existing credentials?"):
                    return
        else:
            # Add the environment
            manager.add_environment(
                env_name, 
                db_type,
                description=f"Imported from PowerShell ({database})",
                is_production=False
            )
        
        # Set credentials
        expiry_days = int(os.environ.get("DB_PWD_EXPIRY", 90))
        manager.set_credentials(
            env_name,
            server,
            port,
            database,
            username,
            password,
            expiry_days,
        )
        
        console.print(f"\n[green]✓ Successfully imported credentials to environment '{env_name}'[/green]")
        
        # Test connection
        if Confirm.ask("\nTest the connection?"):
            console.print("\n[cyan]Testing connection...[/cyan]")
            if manager.test_connection(env_name):
                console.print("[green]✓ Connection test successful![/green]")
            else:
                console.print("[red]✗ Connection test failed![/red]")
                console.print("[yellow]Check that psycopg2 is installed: uv pip install psycopg2-binary[/yellow]")
                
    except Exception as e:
        console.print(f"[red]Error importing credentials: {e}[/red]")
        if "psycopg2" in str(e):
            console.print("\n[yellow]Install psycopg2 with: uv pip install psycopg2-binary[/yellow]")
        sys.exit(1)


if __name__ == "__main__":
    typer.run(main)