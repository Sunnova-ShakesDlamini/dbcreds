# migrate_timezones.py
"""
Script to migrate existing timezone-naive datetimes to timezone-aware.

Run this script to update all existing credentials with timezone-aware datetimes.
"""

import sys
from datetime import datetime, timezone

from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

from dbcreds.core.manager import CredentialManager

console = Console()


def migrate_credentials():
    """Migrate all existing credentials to use timezone-aware datetimes."""
    console.print("[bold blue]Timezone Migration Tool[/bold blue]")
    console.print("This will update all existing credentials to use timezone-aware datetimes.\n")
    
    if not Confirm.ask("Do you want to proceed?"):
        console.print("[yellow]Migration cancelled.[/yellow]")
        return
    
    try:
        manager = CredentialManager()
        environments = manager.list_environments()
        
        if not environments:
            console.print("[yellow]No environments found.[/yellow]")
            return
        
        console.print(f"Found {len(environments)} environments to check.\n")
        
        updated_count = 0
        
        for env in environments:
            try:
                # Get credentials without checking expiry
                creds = manager.get_credentials(env.name, check_expiry=False)
                
                # Check if any datetime fields are naive
                needs_update = False
                
                if creds.password_updated_at and creds.password_updated_at.tzinfo is None:
                    needs_update = True
                
                if creds.password_expires_at and creds.password_expires_at.tzinfo is None:
                    needs_update = True
                
                if needs_update:
                    console.print(f"[yellow]Updating environment: {env.name}[/yellow]")
                    
                    # Re-set the credentials to trigger update with timezone-aware datetimes
                    manager.set_credentials(
                        env.name,
                        host=creds.host,
                        port=creds.port,
                        database=creds.database,
                        username=creds.username,
                        password=creds.password.get_secret_value(),
                        password_expires_days=90  # Default to 90 days
                    )
                    
                    updated_count += 1
                    console.print(f"[green]✓ Updated {env.name}[/green]")
                else:
                    console.print(f"[dim]✓ {env.name} already has timezone-aware datetimes[/dim]")
                    
            except Exception as e:
                console.print(f"[red]✗ Error processing {env.name}: {e}[/red]")
                logger.error(f"Failed to migrate {env.name}: {e}")
        
        console.print(f"\n[bold green]Migration complete![/bold green]")
        console.print(f"Updated {updated_count} environments.")
        
    except Exception as e:
        console.print(f"[red]Migration failed: {e}[/red]")
        logger.exception("Migration failed")
        sys.exit(1)


def check_credentials():
    """Check all credentials for timezone issues."""
    console.print("[bold blue]Checking credentials for timezone issues...[/bold blue]\n")
    
    try:
        manager = CredentialManager()
        environments = manager.list_environments()
        
        issues = []
        
        for env in environments:
            try:
                creds = manager.get_credentials(env.name, check_expiry=False)
                
                naive_fields = []
                if creds.password_updated_at and creds.password_updated_at.tzinfo is None:
                    naive_fields.append("password_updated_at")
                
                if creds.password_expires_at and creds.password_expires_at.tzinfo is None:
                    naive_fields.append("password_expires_at")
                
                if naive_fields:
                    issues.append((env.name, naive_fields))
                    
            except Exception as e:
                logger.debug(f"Error checking {env.name}: {e}")
        
        if issues:
            console.print("[yellow]Found timezone issues in the following environments:[/yellow]\n")
            for env_name, fields in issues:
                console.print(f"  [red]•[/red] {env_name}: {', '.join(fields)}")
            
            console.print("\n[yellow]Run this script with --migrate to fix these issues.[/yellow]")
        else:
            console.print("[green]✓ All credentials have timezone-aware datetimes![/green]")
            
    except Exception as e:
        console.print(f"[red]Check failed: {e}[/red]")
        logger.exception("Check failed")
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate dbcreds to timezone-aware datetimes")
    parser.add_argument("--migrate", action="store_true", help="Perform the migration")
    parser.add_argument("--check", action="store_true", help="Check for timezone issues")
    
    args = parser.parse_args()
    
    if args.migrate:
        migrate_credentials()
    elif args.check:
        check_credentials()
    else:
        # Default to check
        check_credentials()
        console.print("\nRun with --migrate to fix any issues found.")