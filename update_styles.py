#!/usr/bin/env python3
"""
Script to update MkDocs styles and configuration for better color scheme and fix warnings.
Run this in the root folder of the dbcreds project.
"""

import os
from pathlib import Path


def create_file(filepath, content):
    """Create or update a file."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created/Updated {filepath}")


# Updated extra.css with cohesive color scheme
EXTRA_CSS = """/* dbcreds Documentation - Custom Styles */

/* Color Palette Variables */
:root {
  /* Brand Colors */
  --dbcreds-blue: #1E90FF;      /* Vibrant blue from logo */
  --dbcreds-green: #5AC85A;     /* Medium green from logo */
  --dbcreds-light-green: #90EE90; /* Light green from logo */
  --dbcreds-dark-blue: #2F3640;  /* Dark background */
  --dbcreds-gray: #C0C0C0;       /* Gray accent */
  --dbcreds-dark-gray: #4B4B4B;  /* Dark gray */
  
  /* Complementary Colors */
  --dbcreds-teal: #00b8a9;       /* Complementary teal */
  --dbcreds-purple: #6C5CE7;     /* Accent purple */
  --dbcreds-orange: #FFA502;     /* Warning orange */
}

/* Light Mode (Default) */
[data-md-color-scheme="default"] {
  /* Primary colors */
  --md-primary-fg-color: #1E90FF;              /* Main brand blue */
  --md-primary-fg-color--light: #5EB3FF;       /* Lighter blue for hover */
  --md-primary-fg-color--dark: #0066CC;        /* Darker blue for active */
  --md-primary-bg-color: #FFFFFF;
  --md-primary-bg-color--light: #F0F7FF;
  
  /* Accent colors */
  --md-accent-fg-color: #5AC85A;               /* Brand green for accents */
  --md-accent-fg-color--transparent: #5AC85A1A;
  --md-accent-bg-color: #FFFFFF;
  --md-accent-bg-color--light: #F0FFF0;
  
  /* Background colors */
  --md-default-bg-color: #FFFFFF;
  --md-default-bg-color--light: #F8F9FA;
  --md-default-bg-color--lighter: #FEFEFE;
  --md-default-bg-color--lightest: #FFFFFF;
  
  /* Text colors */
  --md-default-fg-color: #212529;               /* Dark gray for text */
  --md-default-fg-color--light: #495057;
  --md-default-fg-color--lighter: #6C757D;
  --md-default-fg-color--lightest: #ADB5BD;
  
  /* Code colors */
  --md-code-fg-color: #E91E63;
  --md-code-bg-color: #F5F5F5;
  --md-code-hl-color: #FFF3CD;
  
  /* Link colors */
  --md-typeset-a-color: #1E90FF;                /* Brand blue for links */
  
  /* Admonition colors */
  --md-admonition-bg-color: #F8F9FA;
  
  /* Footer */
  --md-footer-bg-color: #2F3640;                /* Brand dark blue */
  --md-footer-bg-color--dark: #1A1D23;
  --md-footer-fg-color: #FFFFFF;
  --md-footer-fg-color--light: #E9ECEF;
  --md-footer-fg-color--lighter: #ADB5BD;
  
  /* Custom properties for components */
  --dbcreds-hero-gradient: linear-gradient(135deg, #1E90FF 0%, #5AC85A 100%);
  --dbcreds-card-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  --dbcreds-card-hover-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

/* Dark Mode (Slate) */
[data-md-color-scheme="slate"] {
  /* Primary colors */
  --md-primary-fg-color: #5EB3FF;              /* Lighter blue for dark mode */
  --md-primary-fg-color--light: #90CCFF;
  --md-primary-fg-color--dark: #1E90FF;
  --md-primary-bg-color: #1A1D23;
  --md-primary-bg-color--light: #2F3640;
  
  /* Accent colors */
  --md-accent-fg-color: #90EE90;               /* Light green for dark mode */
  --md-accent-fg-color--transparent: #90EE901A;
  --md-accent-bg-color: #1A1D23;
  --md-accent-bg-color--light: #2F3640;
  
  /* Background colors */
  --md-default-bg-color: #1A1D23;              /* Very dark background */
  --md-default-bg-color--light: #2F3640;       /* Brand dark blue */
  --md-default-bg-color--lighter: #3D4250;
  --md-default-bg-color--lightest: #4A4E5C;
  
  /* Text colors */
  --md-default-fg-color: #E9ECEF;              /* Light gray for text */
  --md-default-fg-color--light: #DEE2E6;
  --md-default-fg-color--lighter: #CED4DA;
  --md-default-fg-color--lightest: #ADB5BD;
  
  /* Code colors */
  --md-code-fg-color: #FF6B9D;
  --md-code-bg-color: #2A2E3A;
  --md-code-hl-color: #3D4250;
  
  /* Link colors */
  --md-typeset-a-color: #5EB3FF;               /* Lighter blue for readability */
  
  /* Admonition colors */
  --md-admonition-bg-color: #2F3640;
  
  /* Footer */
  --md-footer-bg-color: #0F1114;               /* Even darker for footer */
  --md-footer-bg-color--dark: #000000;
  --md-footer-fg-color: #E9ECEF;
  --md-footer-fg-color--light: #CED4DA;
  --md-footer-fg-color--lighter: #ADB5BD;
  
  /* Custom properties for components */
  --dbcreds-hero-gradient: linear-gradient(135deg, #2F3640 0%, #3D4250 100%);
  --dbcreds-card-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  --dbcreds-card-hover-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
}

/* Logo styling */
.md-header__logo img {
  height: 2.5rem;
  border-radius: 20%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s, box-shadow 0.2s;
}

.md-header__logo img:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* Code block improvements */
.highlight pre {
  border-radius: 0.5rem;
  border: 1px solid var(--md-default-fg-color--lightest);
}

/* Fast mode badge */
.fast-mode {
  background-color: var(--dbcreds-teal);
  color: white;
  padding: 0.3rem 0.6rem;
  border-radius: 0.3rem;
  font-size: 0.85rem;
  font-weight: bold;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

/* Hero gradient section */
.hero-gradient {
  background: var(--dbcreds-hero-gradient);
  color: white;
  padding: 4rem 2rem;
  border-radius: 1rem;
  text-align: center;
  margin-bottom: 2rem;
  box-shadow: var(--dbcreds-card-shadow);
}

/* Feature cards */
.feature-card {
  background: var(--md-code-bg-color);
  padding: 1.5rem;
  border-radius: 0.5rem;
  border: 1px solid var(--md-default-fg-color--lightest);
  transition: transform 0.2s, box-shadow 0.2s;
  height: 100%;
}

.feature-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--dbcreds-card-hover-shadow);
}

/* Grid layout */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

/* Announcement bar */
.announcement {
  background: linear-gradient(135deg, var(--dbcreds-teal) 0%, var(--dbcreds-green) 100%);
  color: white;
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 2rem;
  text-align: center;
  box-shadow: var(--dbcreds-card-shadow);
}

.announcement a {
  color: white !important;
  text-decoration: underline;
  font-weight: bold;
}

/* Documentation links */
.doc-link {
  display: block;
  padding: 1.5rem;
  background: var(--md-code-bg-color);
  border-radius: 0.5rem;
  text-decoration: none;
  border: 1px solid var(--md-default-fg-color--lightest);
  transition: transform 0.2s, box-shadow 0.2s;
}

.doc-link:hover {
  transform: translateY(-2px);
  box-shadow: var(--dbcreds-card-hover-shadow);
  text-decoration: none;
}

.doc-link h3 {
  margin: 0;
  color: var(--md-primary-fg-color);
}

.doc-link p {
  margin: 0.5rem 0 0 0;
  color: var(--md-default-fg-color--light);
}

/* Gradient cards for features */
.gradient-card-blue {
  background: linear-gradient(135deg, #1E90FF 0%, #0066CC 100%);
}

.gradient-card-green {
  background: linear-gradient(135deg, #5AC85A 0%, #3CB043 100%);
}

.gradient-card-teal {
  background: linear-gradient(135deg, #00b8a9 0%, #008B7D 100%);
}

.gradient-card-purple {
  background: linear-gradient(135deg, #6C5CE7 0%, #5641D8 100%);
}

/* Tables */
.md-typeset table:not([class]) {
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: var(--dbcreds-card-shadow);
}

.md-typeset table:not([class]) th {
  background-color: var(--md-primary-fg-color);
  color: white;
}

/* Navigation */
.md-nav__link--active {
  color: var(--md-primary-fg-color);
  font-weight: bold;
}

/* Search */
.md-search__form {
  border-radius: 0.5rem;
  overflow: hidden;
}

/* Tabs */
.md-typeset .tabbed-labels label {
  border-radius: 0.5rem 0.5rem 0 0;
}

/* Admonitions */
.md-typeset .admonition {
  border-radius: 0.5rem;
  box-shadow: var(--dbcreds-card-shadow);
}

/* Buttons */
.md-button {
  border-radius: 0.5rem;
  font-weight: 600;
  text-transform: none;
  transition: all 0.2s;
}

.md-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .hero-gradient {
    padding: 3rem 1.5rem;
  }
  
  .hero-gradient h1 {
    font-size: 2rem !important;
  }
  
  .grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}

/* Fix for version selector visibility */
.md-version__current {
  color: var(--md-primary-fg-color);
}

/* Animation for fade effects */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}
"""

# Updated mkdocs.yml to fix versions.json warning
MKDOCS_YML = """# mkdocs.yml
site_name: dbcreds
site_description: Professional Database Credentials Management
site_url: https://sunnova-shakesdlamini.github.io/dbcreds/
repo_url: https://github.com/Sunnova-ShakesDlamini/dbcreds
repo_name: Sunnova-ShakesDlamini/dbcreds
copyright: Copyright &copy; 2024 Sunnova ShakesDlamini

# Theme configuration
theme:
  name: material
  logo: assets/images/logo.svg
  favicon: assets/images/favicon.png
  
  # Color palette configuration
  palette:
    # Light mode
    - scheme: default
      toggle:
        icon: material/weather-night
        name: Switch to dark mode
    
    # Dark mode  
    - scheme: slate
      toggle:
        icon: material/weather-sunny
        name: Switch to light mode
  
  # Font configuration
  font:
    text: Inter
    code: JetBrains Mono
  
  # Features
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.tabs
    - navigation.tabs.sticky
    - navigation.sections
    - navigation.expand
    - navigation.path
    - navigation.indexes
    - navigation.top
    - navigation.footer
    - toc.follow
    - toc.integrate
    - search.suggest
    - search.highlight
    - search.share
    - header.autohide
    - content.code.copy
    - content.code.annotate
    - content.tabs.link
    - announce.dismiss

  icon:
    repo: fontawesome/brands/github

# Custom CSS
extra_css:
  - stylesheets/extra.css

# JavaScript
extra_javascript:
  - javascripts/extra.js

# Plugins configuration
plugins:
  - search:
      separator: '[\s\-\_\.]+'
  - mkdocstrings:
      handlers:
        python:
          options:
            show_source: true
            show_root_heading: true
            show_category_heading: true
            docstring_style: numpy
            merge_init_into_class: true
            show_if_no_docstring: false
            show_signature_annotations: true
            show_bases: true
            heading_level: 2
  # Exclude includes directory from navigation warnings
  - exclude:
      glob:
        - includes/*

# Extensions
markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.snippets:
      base_path: docs
      check_paths: true
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.keys
  - pymdownx.mark
  - pymdownx.smartsymbols
  - pymdownx.tasklist:
      custom_checkbox: true
  - def_list
  - attr_list
  - md_in_html
  - footnotes
  - toc:
      permalink: true
      toc_depth: 3
  - tables
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg

# Page tree
nav:
  - Home: index.md
  - Getting Started:
      - Quickstart: getting-started/quickstart.md
      - Installation: getting-started/installation.md
      - Configuration: getting-started/configuration.md
      - Performance & Lazy Loading: getting-started/performance.md
  - User Guide:
      - CLI Reference: guide/cli.md
      - Python API: guide/python-api.md
      - Web Interface: guide/web-interface.md
      - Storage Backends: guide/backends.md
      - Password Rotation: guide/rotation.md
      - Migration Guide: guide/migration.md
  - Examples:
      - Basic Usage: examples/basic.md
      - SQLAlchemy: examples/sqlalchemy.md
      - Pandas: examples/pandas.md
      - Async Support: examples/async.md
      - Marimo Notebooks: examples/marimo.md
  - Security:
      - Backend Security: security/backends.md
      - Best Practices: security/best-practices.md
  - API Reference:
      - Core: api/core.md
      - Backends: api/backends.md
      - CLI: api/cli.md
      - Web: api/web.md

# Extra configuration
extra:
  # Remove mike versioning to fix versions.json warning
  # Add it back only when you actually use mike for versioning
  # version:
  #   provider: mike
  #   default: latest
  
  # Social links
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/Sunnova-ShakesDlamini
    - icon: fontawesome/brands/python
      link: https://pypi.org/project/dbcreds/
  
  # Analytics (optional)
  analytics:
    provider: google
    property: !ENV GOOGLE_ANALYTICS_KEY
    
  # Homepage
  homepage: https://sunnova-shakesdlamini.github.io/dbcreds/
"""

# Updated index.md with better color usage
INDEX_MD = """# Welcome to dbcreds

<div class="hero-gradient">
  <img src="assets/images/logo.svg" alt="dbcreds logo" width="180" style="margin-bottom: 2rem;">
  
  <h1 style="font-size: 3rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">dbcreds</h1>
  <p style="font-size: 1.5rem; margin-top: 1rem; opacity: 0.95;">Professional Database Credentials Management</p>
  <p style="font-size: 1.1rem; margin-top: 0.5rem;"><span class="fast-mode">⚡ Lightning-Fast Imports!</span></p>
  
  <div style="margin-top: 2rem;">
    <a href="getting-started/quickstart/" class="md-button md-button--primary" style="margin: 0.5rem;">
      Get Started →
    </a>
    <a href="guide/python-api/" class="md-button" style="margin: 0.5rem; background: rgba(255,255,255,0.1); border: 2px solid white;">
      View API Docs
    </a>
  </div>
</div>

<div class="announcement">
  <strong>🎉 New in v2.0:</strong> Intelligent lazy loading for instant imports in Jupyter & marimo notebooks! 
  <a href="getting-started/performance/">Learn more →</a>
</div>

## 🚀 Lightning-Fast Access

<div class="grid">
  
  <div class="feature-card">
    <h3 style="margin-top: 0;">⚡ Instant Imports</h3>
    <p>Automatic marimo detection and lazy loading means imports take milliseconds, not seconds.</p>
    <div class="highlight">
<pre><code class="language-python"># In marimo - automatically fast!
from dbcreds import get_connection_string
conn = get_connection_string("prod")  # ~50ms!</code></pre>
    </div>
  </div>
  
  <div class="feature-card">
    <h3 style="margin-top: 0;">🎯 Smart Detection</h3>
    <p>Detects notebook environments and optimizes automatically. No configuration needed!</p>
    <div class="highlight">
<pre><code class="language-bash"># Force fast mode anywhere
export DBCREDS_FAST_MODE=true
python your_script.py</code></pre>
    </div>
  </div>
  
</div>

## ⚡ Quick Start

```bash
# Install
pip install dbcreds

# Add environment
dbcreds add prod --type postgresql

# Set credentials (stored securely) 
dbcreds set prod --host db.company.com --port 5432 --database myapp --username dbuser

# Use in Python - Lightning fast!
from dbcreds import get_connection_string
conn_string = get_connection_string("prod")
```

## 🔐 Security First

<div class="grid">
  
  <div class="feature-card gradient-card-blue" style="color: white;">
    <h3 style="margin-top: 0; color: white;">🛡️ System Keychains</h3>
    <p>Uses Windows Credential Manager, macOS Keychain, or Linux Secret Service. Your credentials are encrypted by the OS.</p>
  </div>
  
  <div class="feature-card gradient-card-green" style="color: white;">
    <h3 style="margin-top: 0; color: white;">🔑 Zero Plain Text</h3>
    <p>Credentials never touch disk unencrypted. No .env files, no config files with passwords.</p>
  </div>
  
  <div class="feature-card gradient-card-teal" style="color: white;">
    <h3 style="margin-top: 0; color: white;">🔄 Rotation Tracking</h3>
    <p>Built-in password expiry tracking. Get notified before passwords expire.</p>
  </div>
  
</div>

## 🎯 Core Features

<div class="grid">
  
  <div class="feature-card">
    <div style="display: flex; align-items: start;">
      <span style="font-size: 2rem; margin-right: 1rem;">🌍</span>
      <div>
        <h4 style="margin: 0;">Multi-Environment</h4>
        <p style="margin: 0.5rem 0;">Manage dev, staging, and production credentials separately</p>
      </div>
    </div>
  </div>
  
  <div class="feature-card">
    <div style="display: flex; align-items: start;">
      <span style="font-size: 2rem; margin-right: 1rem;">🚀</span>
      <div>
        <h4 style="margin: 0;">Beautiful CLI</h4>
        <p style="margin: 0.5rem 0;">Rich terminal UI with colors, progress bars, and tables</p>
      </div>
    </div>
  </div>
  
  <div class="feature-card">
    <div style="display: flex; align-items: start;">
      <span style="font-size: 2rem; margin-right: 1rem;">🌐</span>
      <div>
        <h4 style="margin: 0;">Web Interface</h4>
        <p style="margin: 0.5rem 0;">FastAPI + HTMX for team credential management</p>
      </div>
    </div>
  </div>
  
  <div class="feature-card">
    <div style="display: flex; align-items: start;">
      <span style="font-size: 2rem; margin-right: 1rem;">📊</span>
      <div>
        <h4 style="margin: 0;">All Databases</h4>
        <p style="margin: 0.5rem 0;">PostgreSQL, MySQL, Oracle, SQL Server, and more</p>
      </div>
    </div>
  </div>
  
  <div class="feature-card">
    <div style="display: flex; align-items: start;">
      <span style="font-size: 2rem; margin-right: 1rem;">🐍</span>
      <div>
        <h4 style="margin: 0;">Python Native</h4>
        <p style="margin: 0.5rem 0;">Works with SQLAlchemy, pandas, asyncio, and more</p>
      </div>
    </div>
  </div>
  
  <div class="feature-card">
    <div style="display: flex; align-items: start;">
      <span style="font-size: 2rem; margin-right: 1rem;">📝</span>
      <div>
        <h4 style="margin: 0;">Type Safe</h4>
        <p style="margin: 0.5rem 0;">Full type hints with Pydantic validation</p>
      </div>
    </div>
  </div>
  
</div>

## 📦 Installation

=== "pip"

    ```bash
    # Basic installation
    pip install dbcreds
    
    # With specific database drivers
    pip install "dbcreds[postgresql,mysql]"
    ```

=== "uv"

    ```bash
    # Fast installation with uv
    uv add dbcreds
    
    # With extras
    uv add "dbcreds[postgresql,mysql]"
    ```

=== "pipx (CLI only)"

    ```bash
    # Install CLI globally
    pipx install dbcreds
    ```

## 💡 Why dbcreds?

<div class="grid">

  <div style="text-align: center;">
    <div style="font-size: 3rem; margin-bottom: 1rem;">🔒</div>
    <h3>Stop Hardcoding</h3>
    <p>No more passwords in code, .env files, or notebooks.</p>
  </div>

  <div style="text-align: center;">
    <div style="font-size: 3rem; margin-bottom: 1rem;">👥</div>
    <h3>Built for Teams</h3>
    <p>Share access without sharing passwords.</p>
  </div>

  <div style="text-align: center;">
    <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
    <h3>Blazing Fast</h3>
    <p>Lazy loading means instant imports.</p>
  </div>

</div>

## 🚀 See It In Action

=== "Basic Usage"

    ```python
    from dbcreds import get_connection_string
    
    # Get connection - it's that simple!
    conn = get_connection_string("prod")
    
    # Use with pandas
    import pandas as pd
    df = pd.read_sql("SELECT * FROM users", conn)
    ```

=== "With SQLAlchemy"

    ```python
    from dbcreds import get_engine
    
    # Get a configured SQLAlchemy engine
    engine = get_engine("analytics")
    
    # Use it normally
    with engine.connect() as conn:
        result = conn.execute("SELECT COUNT(*) FROM events")
        print(f"Total events: {result.scalar()}")
    ```

=== "In Notebooks"

    ```python
    # Automatic fast mode in marimo/Jupyter!
    from dbcreds import get_connection_string
    import pandas as pd
    
    # Lightning fast connection
    df = pd.read_sql(
        "SELECT * FROM daily_metrics", 
        get_connection_string("analytics")
    )
    ```

## 📚 Learn More

<div class="grid">

  <a href="getting-started/quickstart/" class="doc-link">
    <h3>🚀 Quickstart</h3>
    <p>Get up and running in 5 minutes</p>
  </a>

  <a href="getting-started/performance/" class="doc-link">
    <h3>⚡ Performance</h3>
    <p>Learn about lazy loading & fast mode</p>
  </a>

  <a href="guide/cli/" class="doc-link">
    <h3>🖥️ CLI Reference</h3>
    <p>Complete command documentation</p>
  </a>

  <a href="examples/marimo/" class="doc-link">
    <h3>📓 Notebook Examples</h3>
    <p>Using dbcreds in marimo & Jupyter</p>
  </a>

</div>

---

<div style="text-align: center; margin-top: 4rem; padding: 2rem 0;">
  <p style="margin-bottom: 1rem;">Made with 💚 by</p>
  <a href="https://github.com/Sunnova-ShakesDlamini" style="text-decoration: none; font-weight: bold; font-size: 1.1rem;">
    Sunnova ShakesDlamini
  </a>
  <div style="margin-top: 2rem;">
    <a href="https://github.com/Sunnova-ShakesDlamini/dbcreds" style="margin: 0 1rem;">GitHub</a>
    <a href="https://pypi.org/project/dbcreds/" style="margin: 0 1rem;">PyPI</a>
    <a href="https://github.com/Sunnova-ShakesDlamini/dbcreds/issues" style="margin: 0 1rem;">Issues</a>
  </div>
</div>
"""


def main():
    """Apply style updates to dbcreds documentation."""
    print("🎨 Updating dbcreds documentation styles...")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists('mkdocs.yml'):
        print("❌ Error: mkdocs.yml not found. Are you in the dbcreds root directory?")
        return 1
    
    # Update files
    create_file('docs/stylesheets/extra.css', EXTRA_CSS)
    create_file('mkdocs.yml', MKDOCS_YML)
    create_file('docs/index.md', INDEX_MD)
    
    print()
    print("✨ Styles updated successfully!")
    print()
    print("🎨 Key improvements:")
    print("   - Cohesive color scheme for light/dark modes")
    print("   - Brand colors integrated throughout")
    print("   - Better contrast and readability")
    print("   - Fixed versions.json warning")
    print("   - Improved hero section and cards")
    print()
    print("📝 Color scheme details:")
    print("   Light mode: Blue (#1E90FF) primary, Green (#5AC85A) accent")
    print("   Dark mode: Light Blue (#5EB3FF) primary, Light Green (#90EE90) accent")
    print("   Background: White → Dark Blue (#2F3640) in dark mode")
    print()
    print("🚀 Test with: mkdocs serve")
    
    return 0


if __name__ == "__main__":
    exit(main())