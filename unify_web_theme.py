#!/usr/bin/env python3
"""
Script to implement dark mode and ensure template consistency for dbcreds web interface.
"""

import os
from pathlib import Path


def create_file(filepath, content):
    """Create or update a file."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Created/Updated {filepath}")


# Enhanced custom CSS with dark mode support
ENHANCED_CUSTOM_CSS = """/* dbcreds Web Interface - Custom Styles with Dark Mode */

/* Brand Colors */
:root {
  /* Brand Colors */
  --dbcreds-blue: #1E90FF;
  --dbcreds-green: #5AC85A;
  --dbcreds-light-green: #90EE90;
  --dbcreds-dark-blue: #2F3640;
  --dbcreds-gray: #C0C0C0;
  --dbcreds-dark-gray: #4B4B4B;
  --dbcreds-teal: #00b8a9;
  --dbcreds-purple: #6C5CE7;
  --dbcreds-orange: #FFA502;
}

/* Light Mode Variables */
[data-theme="light"] {
  --bg-primary: #FFFFFF;
  --bg-secondary: #F8F9FA;
  --bg-tertiary: #E9ECEF;
  --text-primary: #212529;
  --text-secondary: #495057;
  --text-tertiary: #6C757D;
  --border-color: #DEE2E6;
  --shadow-color: rgba(0, 0, 0, 0.1);
  --card-bg: #FFFFFF;
  --nav-gradient: linear-gradient(135deg, #1E90FF 0%, #2980B9 100%);
  --link-color: #1E90FF;
  --link-hover: #0066CC;
}

/* Dark Mode Variables */
[data-theme="dark"] {
  --bg-primary: #1A1D23;
  --bg-secondary: #2F3640;
  --bg-tertiary: #3D4250;
  --text-primary: #E9ECEF;
  --text-secondary: #CED4DA;
  --text-tertiary: #ADB5BD;
  --border-color: #495057;
  --shadow-color: rgba(0, 0, 0, 0.3);
  --card-bg: #2F3640;
  --nav-gradient: linear-gradient(135deg, #2F3640 0%, #1A1D23 100%);
  --link-color: #5EB3FF;
  --link-hover: #90CCFF;
}

/* Apply theme colors */
body {
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  transition: background-color 0.3s, color 0.3s;
}

/* Navigation */
nav {
  background: var(--nav-gradient);
  transition: background 0.3s;
}

/* Cards */
.card {
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  box-shadow: 0 2px 8px var(--shadow-color);
  transition: all 0.3s;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px var(--shadow-color);
}

/* Buttons */
.btn-primary {
  background: linear-gradient(135deg, #1E90FF 0%, #2980B9 100%);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 600;
  transition: all 0.2s;
  cursor: pointer;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(30, 144, 255, 0.3);
}

.btn-secondary {
  background: linear-gradient(135deg, #5AC85A 0%, #3CB043 100%);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 600;
  transition: all 0.2s;
  cursor: pointer;
}

.btn-secondary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(90, 200, 90, 0.3);
}

/* Theme toggle button */
.theme-toggle {
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  padding: 0.5rem;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s;
}

.theme-toggle:hover {
  background: var(--bg-primary);
  transform: scale(1.05);
}

/* Tables */
table {
  background: var(--card-bg);
  color: var(--text-primary);
}

thead {
  background: linear-gradient(135deg, #1E90FF 0%, #2980B9 100%);
  color: white;
}

[data-theme="dark"] thead {
  background: linear-gradient(135deg, #3D4250 0%, #2F3640 100%);
}

tbody tr {
  border-bottom: 1px solid var(--border-color);
}

tbody tr:hover {
  background: var(--bg-tertiary);
}

/* Forms */
input, select, textarea {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  padding: 0.5rem;
  border-radius: 0.375rem;
  transition: all 0.2s;
}

input:focus, select:focus, textarea:focus {
  border-color: var(--dbcreds-blue);
  outline: none;
  box-shadow: 0 0 0 3px rgba(30, 144, 255, 0.1);
}

[data-theme="dark"] input:focus,
[data-theme="dark"] select:focus,
[data-theme="dark"] textarea:focus {
  box-shadow: 0 0 0 3px rgba(94, 179, 255, 0.1);
}

/* Links */
a {
  color: var(--link-color);
  transition: color 0.2s;
}

a:hover {
  color: var(--link-hover);
}

/* Badges */
.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.badge-success {
  background-color: #5AC85A;
  color: white;
}

.badge-warning {
  background-color: #FFA502;
  color: white;
}

.badge-danger {
  background-color: #E74C3C;
  color: white;
}

.badge-info {
  background-color: #1E90FF;
  color: white;
}

[data-theme="dark"] .badge-success {
  background-color: #3CB043;
}

[data-theme="dark"] .badge-info {
  background-color: #2980B9;
}

/* Modal */
.modal-backdrop {
  background-color: rgba(0, 0, 0, 0.5);
}

[data-theme="dark"] .modal-backdrop {
  background-color: rgba(0, 0, 0, 0.7);
}

.modal-content {
  background: var(--card-bg);
  color: var(--text-primary);
}

/* Fast mode indicator */
.fast-mode-indicator {
  background: linear-gradient(135deg, #00b8a9 0%, #5AC85A 100%);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: bold;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

/* Hero section */
.hero-section {
  background: linear-gradient(135deg, #1E90FF 0%, #5AC85A 100%);
  color: white;
  padding: 2rem;
  border-radius: 1rem;
  text-align: center;
  margin-bottom: 2rem;
  box-shadow: 0 4px 16px var(--shadow-color);
}

[data-theme="dark"] .hero-section {
  background: linear-gradient(135deg, #2F3640 0%, #3D4250 100%);
}

/* Gradient cards */
.gradient-card-blue {
  background: linear-gradient(135deg, #1E90FF 0%, #0066CC 100%);
  color: white;
}

.gradient-card-green {
  background: linear-gradient(135deg, #5AC85A 0%, #3CB043 100%);
  color: white;
}

.gradient-card-teal {
  background: linear-gradient(135deg, #00b8a9 0%, #008B7D 100%);
  color: white;
}

[data-theme="dark"] .gradient-card-blue {
  background: linear-gradient(135deg, #2980B9 0%, #1E90FF 100%);
}

[data-theme="dark"] .gradient-card-green {
  background: linear-gradient(135deg, #3CB043 0%, #5AC85A 100%);
}

[data-theme="dark"] .gradient-card-teal {
  background: linear-gradient(135deg, #008B7D 0%, #00b8a9 100%);
}

/* Loading spinner */
.spinner {
  border: 2px solid var(--bg-tertiary);
  border-top-color: var(--dbcreds-blue);
  border-radius: 50%;
  width: 2rem;
  height: 2rem;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Smooth transitions */
* {
  transition-property: background-color, border-color, color;
  transition-duration: 0.3s;
  transition-timing-function: ease;
}

/* Footer */
footer {
  background: var(--bg-primary);
  border-top: 1px solid var(--border-color);
  color: var(--text-secondary);
}

/* Responsive */
@media (max-width: 768px) {
  .hero-section {
    padding: 1.5rem;
  }
  
  .theme-toggle span {
    display: none;
  }
}
"""

# Updated base.html with dark mode support
DARK_MODE_BASE_HTML = """<!-- dbcreds/web/templates/base.html -->
<!DOCTYPE html>
<html lang="en" class="h-full" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ title }}{% endblock %}</title>
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- HTMX -->
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    
    <!-- Alpine.js for interactivity -->
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    
    <!-- Custom styles -->
    <link rel="stylesheet" href="/static/css/custom.css">
    
    <!-- Theme detection script -->
    <script>
        // Check for saved theme or default to system preference
        const savedTheme = localStorage.getItem('theme') || 
            (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        document.documentElement.setAttribute('data-theme', savedTheme);
    </script>
    
    <!-- Tailwind config -->
    <script>
        tailwind.config = {
            darkMode: ['class', '[data-theme="dark"]'],
            theme: {
                extend: {
                    colors: {
                        'dbcreds-blue': '#1E90FF',
                        'dbcreds-green': '#5AC85A',
                        'dbcreds-light-green': '#90EE90',
                        'dbcreds-dark-blue': '#2F3640',
                        'dbcreds-gray': '#C0C0C0',
                        'dbcreds-dark-gray': '#4B4B4B',
                        'dbcreds-teal': '#00b8a9',
                        'dbcreds-purple': '#6C5CE7',
                        'dbcreds-orange': '#FFA502',
                    }
                }
            }
        }
    </script>
    
    <style>
        [x-cloak] { display: none !important; }
    </style>
</head>
<body class="h-full transition-colors duration-300">
    <div class="min-h-full flex flex-col">
        <!-- Navigation -->
        <nav class="shadow-lg">
            <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div class="flex h-16 justify-between">
                    <div class="flex">
                        <div class="flex flex-shrink-0 items-center">
                            <img src="/static/logo.svg" alt="dbcreds" class="h-8 w-8 mr-2 rounded-lg shadow-md">
                            <h1 class="text-xl font-bold text-white">dbcreds</h1>
                            <span class="ml-3 fast-mode-indicator">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                                </svg>
                                Fast Mode
                            </span>
                        </div>
                        <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
                            <a href="/" class="text-white hover:text-gray-200 inline-flex items-center px-1 pt-1 text-sm font-medium transition-colors">
                                Environments
                            </a>
                            <a href="/settings" class="text-white hover:text-gray-200 inline-flex items-center px-1 pt-1 text-sm font-medium transition-colors">
                                Settings
                            </a>
                        </div>
                    </div>
                    <div class="flex items-center space-x-4">
                        <!-- Theme Toggle -->
                        <button onclick="toggleTheme()" class="theme-toggle" title="Toggle theme">
                            <svg class="w-5 h-5 hidden dark-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>
                            </svg>
                            <svg class="w-5 h-5 light-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>
                            </svg>
                            <span class="ml-2 hidden sm:inline">Theme</span>
                        </button>
                        <span class="text-sm text-gray-200">v{{ version }}</span>
                    </div>
                </div>
            </div>
        </nav>

        <!-- Main content -->
        <main class="flex-grow">
            <div class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
                {% block content %}{% endblock %}
            </div>
        </main>
        
        <!-- Footer -->
        <footer class="mt-auto py-4">
            <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
                <p class="text-sm">
                    Made with 💚 by <a href="https://github.com/Sunnova-ShakesDlamini" class="font-semibold hover:underline">Sunnova ShakesDlamini</a>
                </p>
                <div class="mt-2 space-x-4 text-xs">
                    <a href="https://github.com/Sunnova-ShakesDlamini/dbcreds" class="hover:underline">GitHub</a>
                    <a href="https://pypi.org/project/dbcreds/" class="hover:underline">PyPI</a>
                    <a href="https://sunnova-shakesdlamini.github.io/dbcreds/" class="hover:underline">Docs</a>
                </div>
            </div>
        </footer>
    </div>
    
    <!-- Notification container -->
    <div id="notification-container"></div>
    
    <script>
        // Theme management
        function toggleTheme() {
            const html = document.documentElement;
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcons();
        }
        
        function updateThemeIcons() {
            const theme = document.documentElement.getAttribute('data-theme');
            const darkIcon = document.querySelector('.dark-icon');
            const lightIcon = document.querySelector('.light-icon');
            
            if (theme === 'dark') {
                darkIcon.style.display = 'block';
                lightIcon.style.display = 'none';
            } else {
                darkIcon.style.display = 'none';
                lightIcon.style.display = 'block';
            }
        }
        
        // Initialize theme icons
        updateThemeIcons();
        
        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('theme')) {
                document.documentElement.setAttribute('data-theme', e.matches ? 'dark' : 'light');
                updateThemeIcons();
            }
        });
        
        // Notification system
        function showNotification(message, type = 'success', duration = 3000) {
            const container = document.getElementById('notification-container');
            
            const styles = {
                success: {
                    gradient: 'from-dbcreds-green to-green-600',
                    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>'
                },
                error: {
                    gradient: 'from-red-500 to-red-600',
                    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>'
                },
                warning: {
                    gradient: 'from-dbcreds-orange to-orange-600',
                    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>'
                },
                info: {
                    gradient: 'from-dbcreds-blue to-blue-600',
                    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>'
                }
            };
            
            const style = styles[type] || styles.success;
            
            const notification = document.createElement('div');
            notification.className = 'fixed top-4 right-4 z-50 animate-fade-in-down';
            notification.innerHTML = `
                <div class="bg-gradient-to-r ${style.gradient} text-white px-4 py-3 rounded-lg shadow-lg flex items-center space-x-3 max-w-md">
                    <svg class="h-5 w-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        ${style.icon}
                    </svg>
                    <span class="font-medium">${message}</span>
                    <button onclick="this.parentElement.parentElement.remove()" class="ml-auto -mr-1 p-1 hover:opacity-75">
                        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
            `;
            
            container.insertBefore(notification, container.firstChild);
            
            if (duration > 0) {
                setTimeout(() => {
                    if (notification.parentElement) {
                        notification.classList.add('animate-fade-out-up');
                        setTimeout(() => notification.remove(), 300);
                    }
                }, duration);
            }
        }
    </script>
</body>
</html>
"""

# Updated environment list partial with consistent theme
ENVIRONMENT_LIST_PARTIAL = """<!-- dbcreds/web/templates/partials/environment_list.html -->
{% if environments %}
<div class="overflow-hidden shadow-lg rounded-lg">
    <table class="min-w-full">
        <thead>
            <tr>
                <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-white sm:pl-6">
                    Environment
                </th>
                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-white">
                    Type
                </th>
                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-white">
                    Description
                </th>
                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-white">
                    Password Expiry
                </th>
                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-white">
                    Status
                </th>
                <th scope="col" class="relative py-3.5 pl-3 pr-4 sm:pr-6">
                    <span class="sr-only">Actions</span>
                </th>
            </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
            {% for env in environments %}
            <tr class="hover:bg-gray-50 transition-colors">
                <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium sm:pl-6">
                    {{ env.name }}
                    {% if env.is_production %}
                    <span class="ml-2 inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium badge-danger">
                        Production
                    </span>
                    {% endif %}
                </td>
                <td class="whitespace-nowrap px-3 py-4 text-sm">
                    <span class="badge badge-info">{{ env.database_type.value }}</span>
                </td>
                <td class="whitespace-nowrap px-3 py-4 text-sm">
                    {{ env.description or "-" }}
                </td>
                <td class="whitespace-nowrap px-3 py-4 text-sm" id="expiry-{{ env.name }}">
                    <span class="inline-flex items-center">
                        <svg class="animate-spin h-4 w-4 mr-2 spinner" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Loading...
                    </span>
                </td>
                <td class="whitespace-nowrap px-3 py-4 text-sm">
                    <span class="badge badge-success">
                        Active
                    </span>
                </td>
                <td class="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                    <button hx-get="/environments/{{ env.name }}/edit" 
                            hx-target="#modal"
                            class="text-dbcreds-blue hover:text-blue-700 font-medium mr-3">
                        Edit
                    </button>
                    <button hx-post="/environments/{{ env.name }}/test" 
                            hx-target="#test-result-{{ env.name }}"
                            hx-indicator="#test-indicator-{{ env.name }}"
                            class="text-dbcreds-green hover:text-green-700 font-medium">
                        Test
                    </button>
                    <span id="test-indicator-{{ env.name }}" class="htmx-indicator ml-2">
                        <svg class="animate-spin h-4 w-4 inline spinner" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                    </span>
                    <div id="test-result-{{ env.name }}" class="mt-1"></div>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

<script>
// Load expiry information with better error handling
function loadExpiryInfo(envName) {
    fetch("/api/environments/" + envName + "/expiry")
        .then(response => response.json())
        .then(data => {
            const element = document.getElementById("expiry-" + envName);
            if (!element) return;
            
            let html = '';
            let badgeClass = '';
            
            if (data.error) {
                html = '<span class="badge bg-gray-500 text-white">Error</span>';
            } else if (data.is_expired) {
                html = '<span class="badge badge-danger">Expired</span>';
            } else if (data.days_left !== null) {
                if (data.days_left <= 7) {
                    badgeClass = 'badge-danger';
                } else if (data.days_left <= 30) {
                    badgeClass = 'badge-warning';
                } else {
                    badgeClass = 'badge-success';
                }
                html = `<span class="badge ${badgeClass}">${data.days_left} days left</span>`;
            } else if (data.updated_at && !data.has_expiry) {
                html = '<span class="badge bg-gray-500 text-white">Not tracked</span>';
            } else {
                html = '<span class="badge bg-gray-500 text-white">No expiry</span>';
            }
            
            element.innerHTML = html;
        })
        .catch(error => {
            console.error("Error loading expiry:", error);
            const element = document.getElementById("expiry-" + envName);
            if (element) {
                element.innerHTML = '<span class="badge bg-gray-500 text-white">Error</span>';
            }
        });
}

// Load all expiry info
function loadAllExpiryInfo() {
    {% for env in environments %}
    loadExpiryInfo("{{ env.name }}");
    {% endfor %}
}

// Initial load
document.addEventListener("DOMContentLoaded", loadAllExpiryInfo);
loadAllExpiryInfo();
</script>
{% else %}
<!-- Empty state -->
<div class="card text-center py-12">
    <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path>
    </svg>
    <p class="text-gray-500 mb-4">No environments configured yet.</p>
    <button type="button" 
            class="btn-primary mx-auto"
            hx-get="/environments/new"
            hx-target="#modal">
        Add Your First Environment
    </button>
</div>
{% endif %}
"""

# Consistent modal template for edit/add environment
MODAL_TEMPLATE = """<!-- Modal template structure -->
<div class="fixed z-10 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 modal-backdrop transition-opacity" aria-hidden="true"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
            <div class="modal-content">
                <div class="px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                    <!-- Modal content goes here -->
                </div>
            </div>
        </div>
    </div>
</div>
"""


def main():
    """Implement dark mode and ensure template consistency."""
    print("🌙 Implementing dark mode for dbcreds web interface...")
    print()

    # Check if we're in the right directory
    if not os.path.exists("pyproject.toml"):
        print(
            "❌ Error: pyproject.toml not found. Are you in the dbcreds root directory?"
        )
        return 1

    # Update CSS
    create_file("dbcreds/web/static/css/custom.css", ENHANCED_CUSTOM_CSS)

    # Update templates
    create_file("dbcreds/web/templates/base.html", DARK_MODE_BASE_HTML)
    create_file(
        "dbcreds/web/templates/partials/environment_list.html", ENVIRONMENT_LIST_PARTIAL
    )

    print()
    print("✨ Dark mode implementation complete!")
    print()
    print("🎨 Key features added:")
    print("   - Automatic dark/light mode detection")
    print("   - Manual theme toggle button")
    print("   - Smooth transitions between themes")
    print("   - Consistent color scheme in both modes")
    print("   - Theme preference saved in localStorage")
    print()
    print("🌙 Dark mode colors:")
    print("   - Background: #1A1D23 → #2F3640")
    print("   - Text: #E9ECEF (light gray)")
    print("   - Links: #5EB3FF (light blue)")
    print("   - Cards: #2F3640 with subtle borders")
    print()
    print("☀️  Light mode colors:")
    print("   - Background: #FFFFFF → #F8F9FA")
    print("   - Text: #212529 (dark gray)")
    print("   - Links: #1E90FF (brand blue)")
    print("   - Cards: #FFFFFF with shadows")
    print()
    print("🚀 Restart the web server to see changes:")
    print("   dbcreds-server")

    return 0


if __name__ == "__main__":
    exit(main())
