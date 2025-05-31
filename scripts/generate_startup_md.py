#!/usr/bin/env python
"""
Generate start_up.md file with the latest code from the dbcreds package.
This script automatically discovers and collects all project files.

Usage:
    python generate_startup_md.py [output_file]

Arguments:
    output_file: Optional, path to output file (default: start_up.md)
"""

import argparse
import os
import sys
from collections import defaultdict
from pathlib import Path


class ProjectDocGenerator:
    """Generate documentation by automatically discovering project structure."""

    def __init__(self, project_root=None, exclude_patterns=None):
        self.project_root = Path(
            project_root or os.path.dirname(os.path.abspath(__file__))
        )
        self.exclude_patterns = exclude_patterns or []

        # Default exclusions
        self.default_exclude_dirs = {
            ".git",
            "__pycache__",
            ".pytest_cache",
            ".venv",
            "venv",
            ".idea",
            ".vscode",
            "node_modules",
            ".tox",
            "htmlcov",
            "dist",
            "build",
            "*.egg-info",
            "site",
            "docs/_build",
        }
        self.default_exclude_extensions = {
            ".pyc",
            ".pyo",
            ".pyd",
            ".so",
            ".dll",
            ".dylib",
            ".coverage",
            ".log",
            ".tmp",
            ".bak",
            ".swp",
            ".swo",
        }

        # Special files that should be included at the top
        self.special_files = [
            "pyproject.toml",
            "setup.py",
            "setup.cfg",
            "README.md",
            "LICENSE",
        ]

        # Category patterns for organizing files
        self.category_patterns = {
            "Core": ["core/", "__init__.py"],
            "CLI": ["cli.py", "cli/", "__main__.py"],
            "Web Interface": ["web/", "api/", "routes/"],
            "Backends": ["backends/", "backend/"],
            "Utils": ["utils/", "helpers/", "common/"],
            "Tests": ["test_", "tests/", "spec/"],
            "Config": ["config/", "settings/", "conf/"],
            "Templates": ["templates/", "static/"],
            "Migrations": ["migrate", "migrations/", "alembic/"],
        }

    def should_exclude(self, path):
        """Check if a path should be excluded."""
        path_obj = Path(path)

        # Check directory exclusions
        for part in path_obj.parts:
            if part in self.default_exclude_dirs:
                return True

        # Check extension exclusions
        if path_obj.suffix in self.default_exclude_extensions:
            return True

        # Check custom exclusion patterns
        for pattern in self.exclude_patterns:
            if path_obj.match(pattern):
                return True

        return False

    def categorize_file(self, file_path):
        """Categorize a file based on its path and name."""
        rel_path = Path(file_path).relative_to(self.project_root)
        path_str = str(rel_path).replace("\\", "/")

        # Check each category pattern
        for category, patterns in self.category_patterns.items():
            for pattern in patterns:
                if pattern in path_str.lower():
                    return category

        # Default category based on file location
        parts = rel_path.parts
        if len(parts) > 1:
            # Use the first subdirectory as category
            return parts[1].replace("_", " ").title()
        else:
            return "Root"

    def discover_files(self):
        """Automatically discover all relevant files in the project."""
        files_by_category = defaultdict(list)

        # First, collect special files from root
        for special_file in self.special_files:
            file_path = self.project_root / special_file
            if file_path.exists():
                files_by_category["_PROJECT_CONFIG"].append(str(file_path))

        # Find the main package directory (dbcreds)
        package_dir = None
        for item in self.project_root.iterdir():
            if item.is_dir() and item.name == "dbcreds":
                package_dir = item
                break

        if not package_dir:
            # Try to find any directory with __init__.py
            for item in self.project_root.iterdir():
                if item.is_dir() and (item / "__init__.py").exists():
                    package_dir = item
                    break

        if package_dir:
            # Recursively find all Python files
            for py_file in package_dir.rglob("*.py"):
                if not self.should_exclude(py_file):
                    category = self.categorize_file(py_file)
                    files_by_category[category].append(str(py_file))

            # Find other relevant files (configs, templates, etc.)
            for pattern in ["*.toml", "*.cfg", "*.ini", "*.yaml", "*.yml", "*.json"]:
                for file in package_dir.rglob(pattern):
                    if not self.should_exclude(file):
                        category = self.categorize_file(file)
                        files_by_category[category].append(str(file))

            # Find template files
            for pattern in ["*.html", "*.jinja2", "*.j2"]:
                for file in package_dir.rglob(pattern):
                    if not self.should_exclude(file):
                        files_by_category["Templates"].append(str(file))

        # Sort files within each category
        for category in files_by_category:
            files_by_category[category].sort()

        return dict(files_by_category)

    def generate_directory_tree(self):
        """Generate a visual directory tree."""
        tree_lines = []

        def format_tree(directory, prefix="", is_last=True, level=0):
            if level > 5 or self.should_exclude(directory):
                return

            path = Path(directory)

            # Skip if directory name should be excluded
            if path.name in self.default_exclude_dirs:
                return

            # Add current directory
            if level > 0:
                connector = "└── " if is_last else "├── "
                tree_lines.append(f"{prefix}{connector}{path.name}/")
                prefix += "    " if is_last else "│   "

            # Get and sort contents
            try:
                items = sorted(
                    path.iterdir(), key=lambda x: (not x.is_file(), x.name.lower())
                )
            except PermissionError:
                return

            # Filter items
            items = [item for item in items if not self.should_exclude(item)]

            # Process items
            for i, item in enumerate(items):
                is_last_item = i == len(items) - 1

                if item.is_file():
                    connector = "└── " if is_last_item else "├── "
                    tree_lines.append(f"{prefix}{connector}{item.name}")
                else:
                    format_tree(item, prefix, is_last_item, level + 1)

        # Start from package directory
        package_dir = self.project_root / "dbcreds"
        if package_dir.exists():
            tree_lines.append("dbcreds/")
            format_tree(package_dir, level=0)
        else:
            # Fallback to project root
            tree_lines.append(f"{self.project_root.name}/")
            format_tree(self.project_root, level=0)

        return "\n".join(tree_lines)

    def read_file_content(self, file_path):
        """Read and return the content of a file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Warning: Error reading {file_path}: {e}")
            return f"# Error reading file: {e}"

    def format_code_block(self, file_path, content):
        """Format content as a markdown code block."""
        path = Path(file_path)
        ext = path.suffix.lower()

        # Language mapping
        lang_map = {
            ".py": "python",
            ".toml": "toml",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".json": "json",
            ".ini": "ini",
            ".cfg": "ini",
            ".html": "html",
            ".jinja2": "jinja2",
            ".j2": "jinja2",
            ".js": "javascript",
            ".css": "css",
            ".sh": "bash",
            ".bat": "batch",
            ".ps1": "powershell",
        }

        lang = lang_map.get(ext, "")

        # Special handling for README
        if path.name == "README.md":
            # Strip the first line if it's a title
            lines = content.split("\n")
            if lines and lines[0].startswith("# "):
                content = "\n".join(lines[1:])
            return content

        # Create relative path for display
        try:
            rel_path = path.relative_to(self.project_root)
        except ValueError:
            rel_path = path.name

        return f"```{lang} # {rel_path}\n{content}\n```"

    def generate_documentation(self, output_path):
        """Generate the complete documentation."""
        files_by_category = self.discover_files()
        content = []

        # Header
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content.append(f"# dbcreds Reference\n\nAuto-generated on {timestamp}\n")
        content.append(
            "This file contains the latest source code for the dbcreds library.\n"
        )

        # Directory structure
        content.append("\n## Directory Structure\n")
        content.append(
            "Project organization showing the key files and their relationships:\n"
        )
        content.append(f"\n```\n{self.generate_directory_tree()}\n```")

        # Process special project config files first
        if "_PROJECT_CONFIG" in files_by_category:
            for file_path in files_by_category["_PROJECT_CONFIG"]:
                file_content = self.read_file_content(file_path)
                formatted_content = self.format_code_block(file_path, file_content)
                content.append(formatted_content)
            del files_by_category["_PROJECT_CONFIG"]

        # Define category order
        category_order = [
            "Core",
            "Models",
            "Manager",
            "Exceptions",
            "Backend Implementations",
            "Backends",
            "Web Interface",
            "Web",
            "Api",
            "Routes",
            "Utility Functions",
            "Utils",
            "Helpers",
            "Command-Line Interface",
            "CLI",
            "Migrations",
            "Migrate",
            "Config",
            "Settings",
            "Templates",
        ]

        # Process categories in order
        processed_categories = set()

        for category in category_order:
            if category in files_by_category and files_by_category[category]:
                # Format category name for display
                display_name = category.replace("_", " ")
                content.append(f"\n## {display_name}\n")

                for file_path in sorted(files_by_category[category]):
                    file_content = self.read_file_content(file_path)
                    formatted_content = self.format_code_block(file_path, file_content)
                    content.append(formatted_content)

                processed_categories.add(category)

        # Process any remaining categories
        for category, files in sorted(files_by_category.items()):
            if category not in processed_categories and files:
                display_name = category.replace("_", " ")
                content.append(f"\n## {display_name}\n")

                for file_path in sorted(files):
                    file_content = self.read_file_content(file_path)
                    formatted_content = self.format_code_block(file_path, file_content)
                    content.append(formatted_content)

        # Write output
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(content))

        # Summary statistics
        total_files = sum(len(files) for files in files_by_category.values())
        total_categories = len(files_by_category)

        return total_files, total_categories


def main():
    """Parse command line arguments and generate the documentation."""
    parser = argparse.ArgumentParser(
        description="Generate start_up.md with all project code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_startup_md.py
  python generate_startup_md.py output.md
  python generate_startup_md.py -e "*.test.py" "temp/*"
  python generate_startup_md.py --root /path/to/project
        """,
    )

    parser.add_argument(
        "output_file",
        nargs="?",
        default="start_up.md",
        help="Output markdown file name (default: start_up.md)",
    )
    parser.add_argument(
        "-e",
        "--exclude",
        nargs="+",
        default=[],
        help='Files or patterns to exclude (e.g. "*.test.py")',
    )
    parser.add_argument(
        "-r",
        "--root",
        default=None,
        help="Project root directory (default: current directory)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show verbose output"
    )

    args = parser.parse_args()

    # Create generator
    generator = ProjectDocGenerator(
        project_root=args.root, exclude_patterns=args.exclude
    )

    # Generate documentation
    try:
        total_files, total_categories = generator.generate_documentation(
            args.output_file
        )

        print(f"✓ Generated {args.output_file} successfully!")
        print(f"✓ Included {total_files} files across {total_categories} categories")
        print(f"✓ File size: {os.path.getsize(args.output_file) / 1024:.1f} KB")

        if args.verbose:
            print(f"\nProject root: {generator.project_root}")
            print(f"Exclusions: {generator.exclude_patterns}")

    except Exception as e:
        print(f"✗ Error generating documentation: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
