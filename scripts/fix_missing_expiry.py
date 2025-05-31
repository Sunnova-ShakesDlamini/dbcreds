# fix_missing_expiry.py
"""
Quick fix script to add missing password_expires_at dates to environments
that have password_updated_at but no expiry date.
"""

from datetime import timedelta, timezone

from rich.console import Console

from dbcreds.core.manager import CredentialManager

console = Console()


def fix_environment_expiry(env_name: str, expiry_days: int = 90):
    """Fix missing expiry date for a specific environment."""
    try:
        manager = CredentialManager()

        # Get current credentials
        creds = manager.get_credentials(env_name, check_expiry=False)

        console.print(f"\n[bold]Environment: {env_name}[/bold]")
        console.print(f"Password updated at: {creds.password_updated_at}")
        console.print(f"Password expires at: {creds.password_expires_at}")

        if creds.password_expires_at is None and creds.password_updated_at:
            console.print("\n[yellow]Missing expiry date detected. Fixing...[/yellow]")

            # Ensure timezone aware
            updated_at = creds.password_updated_at
            if updated_at.tzinfo is None:
                updated_at = updated_at.replace(tzinfo=timezone.utc)

            # Calculate expiry date
            expires_at = updated_at + timedelta(days=expiry_days)

            console.print(
                f"Setting expiry to: {expires_at} ({expiry_days} days from update date)"
            )

            # Update the credentials with the same data but trigger expiry calculation
            manager.set_credentials(
                env_name,
                host=creds.host,
                port=creds.port,
                database=creds.database,
                username=creds.username,
                password=creds.password.get_secret_value(),
                password_expires_days=expiry_days,
            )

            # Verify the fix
            updated_creds = manager.get_credentials(env_name, check_expiry=False)
            console.print(
                f"\n[green]✓ Fixed! New expiry date: {updated_creds.password_expires_at}[/green]"
            )

            days_left = updated_creds.days_until_expiry()
            if days_left is not None:
                console.print(f"[green]Days until expiry: {days_left}[/green]")

        else:
            console.print(
                "\n[green]✓ This environment already has an expiry date set.[/green]"
            )

    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        import traceback

        traceback.print_exc()


def check_all_environments():
    """Check all environments for missing expiry dates."""
    try:
        manager = CredentialManager()
        environments = manager.list_environments()

        console.print(
            "[bold]Checking all environments for missing expiry dates...[/bold]\n"
        )

        missing_expiry = []

        for env in environments:
            try:
                creds = manager.get_credentials(env.name, check_expiry=False)

                if creds.password_updated_at and creds.password_expires_at is None:
                    missing_expiry.append(env.name)
                    console.print(
                        f"[yellow]• {env.name} - Missing expiry date[/yellow]"
                    )
                else:
                    console.print(f"[green]✓ {env.name} - OK[/green]")

            except Exception as e:
                console.print(f"[red]✗ {env.name} - Error: {e}[/red]")

        if missing_expiry:
            console.print(
                f"\n[yellow]Found {len(missing_expiry)} environments missing expiry dates:[/yellow]"
            )
            for name in missing_expiry:
                console.print(f"  • {name}")
            console.print(
                "\n[yellow]Run this script with --fix-all to fix all of them.[/yellow]"
            )
        else:
            console.print("\n[green]✓ All environments have expiry dates set![/green]")

        return missing_expiry

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return []


def fix_all_missing():
    """Fix all environments with missing expiry dates."""
    missing = check_all_environments()

    if missing:
        console.print(f"\n[bold]Fixing {len(missing)} environments...[/bold]")

        for env_name in missing:
            console.print(f"\n{'=' * 50}")
            fix_environment_expiry(env_name)

        console.print("\n[bold green]All environments fixed![/bold green]")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fix missing password expiry dates")
    parser.add_argument("environment", nargs="?", help="Environment name to fix")
    parser.add_argument(
        "--expiry-days",
        type=int,
        default=90,
        help="Days until password expires (default: 90)",
    )
    parser.add_argument("--check", action="store_true", help="Check all environments")
    parser.add_argument(
        "--fix-all",
        action="store_true",
        help="Fix all environments with missing expiry",
    )

    args = parser.parse_args()

    if args.check:
        check_all_environments()
    elif args.fix_all:
        fix_all_missing()
    elif args.environment:
        fix_environment_expiry(args.environment, args.expiry_days)
    else:
        # Default to checking all
        check_all_environments()
        console.print("\nUsage:")
        console.print(
            "  python fix_missing_expiry.py fusionods        # Fix specific environment"
        )
        console.print(
            "  python fix_missing_expiry.py --check          # Check all environments"
        )
        console.print(
            "  python fix_missing_expiry.py --fix-all        # Fix all missing expiry dates"
        )
