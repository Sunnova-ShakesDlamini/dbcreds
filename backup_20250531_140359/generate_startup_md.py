#!/usr/bin/env python
"""
Generate start_up.md file with the latest code from the dbcreds package.
This script collects essential project files and combines them into a single markdown file.

Usage:
    python generate_startup_md.py [output_file]
    
Arguments:
    output_file: Optional, path to output file (default: start_up.md)
"""

import os
import sys
import glob
import argparse
from pathlib import Path


def generate_directory_structure():
    """Generate a markdown representation of the dbcreds directory structure."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dbcreds_dir = os.path.join(base_dir, "dbcreds")
    
    if not os.path.exists(dbcreds_dir):
        return "Error: dbcreds directory not found"
    
    # Skip these directories and files when generating tree
    skip_dirs = [".git", "__pycache__", ".pytest_cache", ".venv", ".idea", ".vscode"]
    skip_extensions = [".pyc", ".pyo", ".pyd", ".so", ".dll"]
    
    def format_tree(directory, prefix="", is_last=True, level=0):
        if os.path.basename(directory) in skip_dirs:
            return ""
            
        # Limit to depth of 5 to prevent too much detail
        if level > 5:
            return ""
            
        output = []
        basename = os.path.basename(directory)
        
        # Skip root directory name
        if level > 0:
            connector = "└── " if is_last else "├── "
            output.append(f"{prefix}{connector}{basename}/")
            prefix += "    " if is_last else "│   "
        
        items = [os.path.join(directory, item) for item in sorted(os.listdir(directory))]
        dirs = [item for item in items if os.path.isdir(item)]
        files = [item for item in items if os.path.isfile(item)]
        
        # Filter out unwanted directories
        dirs = [d for d in dirs if os.path.basename(d) not in skip_dirs]
        
        # Filter out unwanted files
        files = [f for f in files if not any(f.endswith(ext) for ext in skip_extensions)]
        
        # Process all files first
        for i, file_path in enumerate(files):
            file_name = os.path.basename(file_path)
            is_file_last = (i == len(files) - 1) and len(dirs) == 0
            connector = "└── " if is_file_last else "├── "
            output.append(f"{prefix}{connector}{file_name}")
        
        # Then process directories
        for i, dir_path in enumerate(dirs):
            is_dir_last = i == len(dirs) - 1
            output.append(format_tree(dir_path, prefix, is_dir_last, level + 1))
        
        return "\n".join(output)
    
    tree = format_tree(dbcreds_dir, level=0)
    return f"```\ndbcreds/\n{tree}\n```"


def collect_key_files(exclude_patterns=None):
    """
    Collect paths of key project files to include in documentation.
    
    Args:
        exclude_patterns: List of glob patterns to exclude
        
    Returns:
        Dictionary of file categories with their file paths
    """
    # Initialize empty exclusion list if none provided
    exclude_patterns = exclude_patterns or []
    
    # Define files to include
    files = {
        "PROJECT_CONFIG": ["pyproject.toml", "README.md"],
        "CORE_MODULES": [
            "dbcreds/__init__.py",
            "dbcreds/core/__init__.py",
            "dbcreds/core/models.py",
            "dbcreds/core/manager.py",
            "dbcreds/core/exceptions.py",
        ],
        "WEB_MODULES": [
            "dbcreds/web/__init__.py",
            "dbcreds/web/__main__.py",
            "dbcreds/web/main.py",
            "dbcreds/web/errors.py",
        ],
        "BACKENDS": [
            "dbcreds/backends/base.py",
            "dbcreds/backends/config.py",
            "dbcreds/backends/windows.py",
            "dbcreds/backends/keyring.py",
            "dbcreds/backends/environment.py",
            "dbcreds/backends/legacy_windows.py",
        ],
        "UTILS": [
            "dbcreds/utils/shortcuts.py",
        ],
        "CLI": [
            "dbcreds/cli.py",
            "dbcreds/migrate.py",
        ],
    }
    
    # Convert to absolute paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check exclusions for each file and filter out matches
    for category, file_list in files.items():
        abs_paths = []
        for f in file_list:
            abs_path = os.path.join(base_dir, f)
            # Check if file should be excluded
            if not any(Path(abs_path).match(pattern) for pattern in exclude_patterns):
                abs_paths.append(abs_path)
            else:
                print(f"Excluding: {f}")
        files[category] = abs_paths
    
    return files


def read_file_content(file_path):
    """Read and return the content of a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return f"# Error reading {os.path.basename(file_path)}"


def format_code_block(file_path, content):
    """Format content as a markdown code block with appropriate language."""
    file_ext = os.path.splitext(file_path)[1]
    lang = ""
    
    if file_ext == '.py':
        lang = "python"
    elif file_ext == '.toml':
        lang = "toml"
    elif file_ext == '.md':
        # For README.md, just return the content without code block
        if file_path.endswith('README.md'):
            return content
        lang = "markdown"
    elif file_ext == '.html':
        lang = "html"
    elif file_ext == '.js':
        lang = "javascript"
    elif file_ext == '.css':
        lang = "css"
    else:
        # Default if we can't determine
        lang = ""
    
    # Create a relative path for display
    rel_path = file_path.replace(os.path.dirname(os.path.abspath(__file__)), '')
    if rel_path.startswith(('/', '\\')):  # Remove leading slash
        rel_path = rel_path[1:]
    
    # For non-README.md files, create a code block with file path
    if file_path.endswith('README.md'):
        return content
    else:
        return f"```{lang} # {rel_path}\n{content}\n```"


def generate_startup_md(output_path, exclude_patterns=None):
    """
    Generate the start_up.md file with all project code.
    
    Args:
        output_path: Path to output file
        exclude_patterns: List of patterns to exclude
    """
    files = collect_key_files(exclude_patterns)
    content = []
    
    # Add header
    from datetime import datetime
    timestamp = os.path.getmtime(files["PROJECT_CONFIG"][0]) if os.path.exists(files["PROJECT_CONFIG"][0]) else None
    date_str = "Unknown" if timestamp is None else datetime.fromtimestamp(Path(__file__).stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    content.append(f"# dbcreds Reference\n\nAuto-generated on {date_str}\n\nThis file contains the latest source code for the dbcreds library.\n")
    
    # Add directory structure as the first item after the header
    content.append("## Directory Structure\n\nProject organization showing the key files and their relationships:\n")
    content.append(generate_directory_structure())
    
    # Start with project config files
    for file_path in files["PROJECT_CONFIG"]:
        if os.path.exists(file_path):
            file_content = read_file_content(file_path)
            if file_path.endswith('README.md'):
                # For README, extract the content excluding the title (first line)
                lines = file_content.split('\n')
                if lines and lines[0].startswith('# '):
                    file_content = '\n'.join(lines[1:])
                content.append(f"# Project Documentation\n\n{file_content}")
            else:
                content.append(format_code_block(file_path, file_content))
    
    # Add core modules
    content.append("\n## Core Modules\n")
    for file_path in files["CORE_MODULES"]:
        if os.path.exists(file_path):
            file_content = read_file_content(file_path)
            content.append(format_code_block(file_path, file_content))
    
    # Add backend implementations
    content.append("\n## Backend Implementations\n")
    for file_path in files["BACKENDS"]:
        if os.path.exists(file_path):
            file_content = read_file_content(file_path)
            content.append(format_code_block(file_path, file_content))
    
    # Add web modules
    content.append("\n## Web Interface\n")
    for file_path in files["WEB_MODULES"]:
        if os.path.exists(file_path):
            file_content = read_file_content(file_path)
            content.append(format_code_block(file_path, file_content))

    # Add utility functions
    content.append("\n## Utility Functions\n")
    for file_path in files["UTILS"]:
        if os.path.exists(file_path):
            file_content = read_file_content(file_path)
            content.append(format_code_block(file_path, file_content))

    # Add CLI modules
    content.append("\n## Command-Line Interface\n")
    for file_path in files["CLI"]:
        if os.path.exists(file_path):
            file_content = read_file_content(file_path)
            content.append(format_code_block(file_path, file_content))
    
    # Write the combined content to the output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(content))
    
    print(f"Generated {output_path} successfully!")
    print(f"Included {sum(len(files[k]) for k in files)} files.")


def main():
    """Parse command line arguments and generate the documentation."""
    parser = argparse.ArgumentParser(description='Generate start_up.md with all project code')
    parser.add_argument('output_file', nargs='?', default='start_up.md',
                        help='Output markdown file name (default: start_up.md)')
    parser.add_argument('-e', '--exclude', nargs='+', default=[],
                        help='Files or patterns to exclude (e.g. "*.test.py")')
    args = parser.parse_args()
    
    generate_startup_md(args.output_file, args.exclude)
    
    print(f"✓ Generated {args.output_file} successfully!")
    print(f"✓ File size: {os.path.getsize(args.output_file) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
