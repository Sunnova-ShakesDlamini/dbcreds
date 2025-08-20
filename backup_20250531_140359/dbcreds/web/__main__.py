# dbcreds/web/__main__.py
"""Entry point for dbcreds-server command."""

import sys

from rich.console import Console

from dbcreds.web.main import run_server

console = Console()


def main():
    """Run the dbcreds web server."""
    try:
        run_server()
    except KeyboardInterrupt:
        console.print("\n[yellow]Server stopped by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]Failed to start server:[/bold red] {e}")
        console.print_exception()
        sys.exit(1)


if __name__ == "__main__":
    main()