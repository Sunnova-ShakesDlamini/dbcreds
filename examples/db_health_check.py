# db_health_check.py
"""Monitor database health across all environments."""

import time
from datetime import datetime
from dbcreds import CredentialManager, get_connection
import smtplib
from email.mime.text import MIMEText

def check_database_health(env_name):
    """Check if database is responsive."""
    start_time = time.time()
    
    try:
        with get_connection(env_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            
        response_time = (time.time() - start_time) * 1000  # ms
        return {
            'status': 'healthy',
            'response_time': round(response_time, 2),
            'error': None
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'response_time': None,
            'error': str(e)
        }

def check_all_environments():
    """Check health of all database environments."""
    manager = CredentialManager()
    results = {}
    
    for env in manager.list_environments():
        print(f"Checking {env.name}...")
        results[env.name] = check_database_health(env.name)
    
    return results

def send_alert(results):
    """Send email alert for unhealthy databases."""
    unhealthy = [
        f"{env}: {info['error']}"
        for env, info in results.items()
        if info['status'] == 'unhealthy'
    ]
    
    if not unhealthy:
        return
    
    # Configure your email settings
    msg = MIMEText(
        f"The following databases are unhealthy:\n\n" +
        "\n".join(unhealthy)
    )
    msg['Subject'] = 'Database Health Alert'
    msg['From'] = 'monitoring@yourcompany.com'
    msg['To'] = 'ops@yourcompany.com'
    
    # Send email (configure SMTP server)
    # server = smtplib.SMTP('smtp.yourcompany.com')
    # server.send_message(msg)
    # server.quit()

def main():
    """Run health checks and report results."""
    print(f"Database Health Check - {datetime.now()}")
    print("-" * 50)
    
    results = check_all_environments()
    
    # Print results
    for env, info in results.items():
        if info['status'] == 'healthy':
            print(f"✓ {env}: {info['response_time']}ms")
        else:
            print(f"✗ {env}: {info['error']}")
    
    # Send alerts if needed
    send_alert(results)
    
    # Return exit code based on health
    unhealthy_count = sum(
        1 for info in results.values() 
        if info['status'] == 'unhealthy'
    )
    
    return unhealthy_count

if __name__ == "__main__":
    exit(main())
