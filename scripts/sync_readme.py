#!/usr/bin/env python3
"""
Sync README.md content with docs/index.md while preserving the beautiful homepage design.

This script extracts specific sections from README.md and updates corresponding
sections in the homepage, maintaining all the styling and layout.
"""

import re
from pathlib import Path
from typing import Dict, Optional


def extract_readme_sections(readme_path: Path) -> Dict[str, str]:
    """Extract specific sections from README.md."""
    content = readme_path.read_text(encoding='utf-8')
    
    sections = {}
    
    # Extract installation section
    install_match = re.search(
        r'## Installation\s*\n(.*?)(?=\n##|\Z)', 
        content, 
        re.DOTALL
    )
    if install_match:
        sections['installation'] = install_match.group(1).strip()
    
    # Extract features section
    features_match = re.search(
        r'## Features\s*\n(.*?)(?=\n##|\Z)', 
        content, 
        re.DOTALL
    )
    if features_match:
        sections['features'] = features_match.group(1).strip()
    
    # Extract quick start section
    quickstart_match = re.search(
        r'## Quick Start\s*\n(.*?)(?=\n##|\Z)', 
        content, 
        re.DOTALL
    )
    if quickstart_match:
        sections['quickstart'] = quickstart_match.group(1).strip()
    
    return sections


def update_homepage_section(homepage_content: str, section_name: str, new_content: str) -> str:
    """Update a specific section in the homepage while preserving styling."""
    
    if section_name == 'quickstart':
        # Find and replace the Quick Start code block
        pattern = r'(## ⚡ Quick Start\s*\n\n```bash\n)(.*?)(```)'
        
        # Extract just the bash commands from new content
        bash_match = re.search(r'```bash\n(.*?)```', new_content, re.DOTALL)
        if bash_match:
            bash_content = bash_match.group(1).strip()
            # Ensure GitHub URL is correct
            bash_content = bash_content.replace(
                'yourcompany/dbcreds',
                'Sunnova-ShakesDlamini/dbcreds'
            )
            replacement = rf'\g<1>{bash_content}\n\g<3>'
            homepage_content = re.sub(pattern, replacement, homepage_content, flags=re.DOTALL)
    
    elif section_name == 'installation':
        # Update installation tabs
        # Extract installation commands from README
        pip_match = re.search(r'pip install ([^\n]+)', new_content)
        if pip_match:
            install_cmd = pip_match.group(1).strip()
            # Ensure GitHub URL is correct
            install_cmd = install_cmd.replace(
                'yourcompany/dbcreds',
                'Sunnova-ShakesDlamini/dbcreds'
            )
            
            # Update pip section
            pattern = r'(=== "pip"\s*\n\s*```bash\s*\n\s*pip install )[^\n]+(.*?```)'
            homepage_content = re.sub(
                pattern, 
                rf'\g<1>{install_cmd}\g<2>', 
                homepage_content, 
                flags=re.DOTALL
            )
            
            # Update uv section
            pattern = r'(=== "uv"\s*\n\s*```bash\s*\n\s*uv pip install )[^\n]+(.*?```)'
            homepage_content = re.sub(
                pattern, 
                rf'\g<1>{install_cmd}\g<2>', 
                homepage_content, 
                flags=re.DOTALL
            )
    
    return homepage_content


def sync_readme_to_homepage(readme_path: Path, homepage_path: Path, dry_run: bool = False):
    """Sync README content to homepage while preserving design."""
    
    # Read files
    readme_sections = extract_readme_sections(readme_path)
    homepage_content = homepage_path.read_text(encoding='utf-8')
    original_content = homepage_content
    
    # Update sections
    for section_name, section_content in readme_sections.items():
        homepage_content = update_homepage_section(homepage_content, section_name, section_content)
    
    # Show diff or write file
    if homepage_content != original_content:
        if dry_run:
            print("Changes to be made:")
            print("-" * 50)
            # Simple diff display
            for line in homepage_content.splitlines():
                if line not in original_content:
                    print(f"+ {line}")
        else:
            homepage_path.write_text(homepage_content, encoding='utf-8')
            print(f"✅ Updated {homepage_path}")
    else:
        print("ℹ️  No changes needed")


def create_readme_includes():
    """
    Alternative approach: Create include files for shared content.
    This allows using the same content in both README and docs.
    """
    
    includes_dir = Path("docs/includes")
    includes_dir.mkdir(exist_ok=True)
    
    # Create a shared installation snippet
    installation_content = """
<!-- docs/includes/installation.md -->
Install directly from GitHub using pip:

```bash
pip install git+https://github.com/Sunnova-ShakesDlamini/dbcreds.git
```

Or using uv:

```bash
uv pip install git+https://github.com/Sunnova-ShakesDlamini/dbcreds.git
```

For development with additional database support:

```bash
# PostgreSQL only (default)
pip install git+https://github.com/Sunnova-ShakesDlamini/dbcreds.git

# With MySQL support
pip install "git+https://github.com/Sunnova-ShakesDlamini/dbcreds.git#egg=dbcreds[mysql]"

# With all databases
pip install "git+https://github.com/Sunnova-ShakesDlamini/dbcreds.git#egg=dbcreds[mysql,oracle,mssql]"
```
"""
    
    (includes_dir / "installation.md").write_text(installation_content.strip())
    
    print(f"✅ Created includes directory at {includes_dir}")
    print("\nTo use in your documentation:")
    print("In README.md: Copy the content directly")
    print("In docs files: Use {% include 'includes/installation.md' %}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Sync README to homepage")
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Show what would be changed without modifying files"
    )
    parser.add_argument(
        "--create-includes",
        action="store_true",
        help="Create include files for shared content"
    )
    
    args = parser.parse_args()
    
    if args.create_includes:
        create_readme_includes()
    else:
        readme_path = Path("README.md")
        homepage_path = Path("docs/index.md")
        
        if not readme_path.exists():
            print(f"❌ Error: {readme_path} not found")
            exit(1)
        
        if not homepage_path.exists():
            print(f"❌ Error: {homepage_path} not found")
            exit(1)
        
        sync_readme_to_homepage(readme_path, homepage_path, args.dry_run)