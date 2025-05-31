# Welcome to dbcreds

<div class="hero-gradient">
  <img src="assets/images/logo.svg" alt="dbcreds logo" width="200" style="margin-bottom: 2rem; border-radius: 20%; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);">
  
  <h1 style="font-size: 3rem; margin: 0;">dbcreds</h1>
  <p style="font-size: 1.5rem; margin-top: 1rem; opacity: 0.9;">Professional Database Credentials Management</p>
  
  <div style="margin-top: 2rem;">
    <a href="getting-started/quickstart/" class="md-button md-button--primary" style="margin: 0.5rem;">
      Get Started →
    </a>
    <a href="guide/cli/" class="md-button" style="margin: 0.5rem; background: transparent; border: 2px solid white;">
      View Documentation
    </a>
  </div>
</div>

## 🔐 Secure by Design

<div class="grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; margin: 2rem 0;">
  
  <div class="feature-card">
    <h3>🛡️ Multiple Storage Backends</h3>
    <p>Leverage your system's native credential store - Windows Credential Manager, macOS Keychain, or Linux Secret Service.</p>
  </div>
  
  <div class="feature-card">
    <h3>🔑 Never Plain Text</h3>
    <p>Credentials are encrypted at rest using industry-standard encryption. Your passwords never touch disk in plain text.</p>
  </div>
  
  <div class="feature-card">
    <h3>🔄 Password Rotation Tracking</h3>
    <p>Built-in password expiry tracking with notifications. Never forget to rotate credentials again.</p>
  </div>
  
</div>

## ⚡ Quick Start

--8<-- "includes/quickstart.md"

## 🎯 Key Features

<div class="grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; margin: 2rem 0;">
  
  <div class="feature-card">
    <h3>🌍 Multi-Environment</h3>
    <p>Manage credentials for development, staging, and production environments with ease.</p>
  </div>
  
  <div class="feature-card">
    <h3>🚀 Rich CLI</h3>
    <p>Beautiful command-line interface built with Rich and Typer for a delightful developer experience.</p>
  </div>
  
  <div class="feature-card">
    <h3>🌐 Web Interface</h3>
    <p>Optional FastAPI web interface for team collaboration and visual credential management.</p>
  </div>
  
  <div class="feature-card">
    <h3>📊 Multi-Database</h3>
    <p>Support for PostgreSQL, MySQL, Oracle, SQL Server, and more.</p>
  </div>
  
  <div class="feature-card">
    <h3>🐍 Python First</h3>
    <p>Seamless integration with SQLAlchemy, pandas, and async frameworks.</p>
  </div>
  
  <div class="feature-card">
    <h3>📝 Type Safe</h3>
    <p>Full type hints with Pydantic models for reliable, maintainable code.</p>
  </div>
  
</div>

## 📚 Documentation

- **[Quickstart Guide](getting-started/quickstart.md)** - Get up and running in 5 minutes
- **[CLI Reference](guide/cli.md)** - Complete command-line documentation
- **[Python API](guide/python-api.md)** - Use dbcreds in your Python applications
- **[Web Interface](guide/web-interface.md)** - Set up the team collaboration interface
- **[API Reference](api/core.md)** - Detailed API documentation

## 🔧 Installation

--8<-- "includes/installation-tabs.md"

## 💡 Why dbcreds?

!!! tip "Stop hardcoding credentials"
    No more passwords in code, environment files, or notebooks. dbcreds provides a secure, 
    centralized way to manage database credentials across all your projects.

!!! info "Built for teams"
    With the web interface, team members can securely share access to development and staging 
    databases without sharing passwords directly.

!!! success "Production ready"
    Used in production environments with support for password rotation policies, audit logging, 
    and enterprise security requirements.

---

<div style="text-align: center; margin-top: 4rem; opacity: 0.7;">
  Made with 💚 by <a href="https://github.com/Sunnova-ShakesDlamini" style="color: var(--dbcreds-teal);">Sunnova ShakesDlamini</a>
</div>