# Welcome to dbcreds

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
