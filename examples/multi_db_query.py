# multi_db_query.py
"""Execute queries across multiple database environments."""

import argparse
import json
from tabulate import tabulate
from dbcreds import get_connection, CredentialManager

def execute_query(env_name, query):
    """Execute a query on a specific environment."""
    try:
        with get_connection(env_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            
            # Get column names
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            
            # Fetch results
            results = cursor.fetchall() if columns else []
            
            return {
                'success': True,
                'columns': columns,
                'rows': results,
                'error': None
            }
    except Exception as e:
        return {
            'success': False,
            'columns': [],
            'rows': [],
            'error': str(e)
        }

def main():
    parser = argparse.ArgumentParser(description='Execute queries across environments')
    parser.add_argument('query', help='SQL query to execute')
    parser.add_argument(
        '--envs', 
        nargs='+', 
        help='Environments to query (default: all)'
    )
    parser.add_argument(
        '--output', 
        choices=['table', 'json', 'csv'],
        default='table',
        help='Output format'
    )
    
    args = parser.parse_args()
    
    # Get environments
    manager = CredentialManager()
    if args.envs:
        environments = args.envs
    else:
        environments = [env.name for env in manager.list_environments()]
    
    # Execute query on each environment
    all_results = {}
    for env in environments:
        print(f"Querying {env}...")
        all_results[env] = execute_query(env, args.query)
    
    # Display results
    for env, result in all_results.items():
        print(f"\n=== {env.upper()} ===")
        
        if result['success']:
            if result['rows']:
                if args.output == 'table':
                    print(tabulate(
                        result['rows'], 
                        headers=result['columns'],
                        tablefmt='grid'
                    ))
                elif args.output == 'json':
                    data = [
                        dict(zip(result['columns'], row))
                        for row in result['rows']
                    ]
                    print(json.dumps(data, indent=2, default=str))
                elif args.output == 'csv':
                    print(','.join(result['columns']))
                    for row in result['rows']:
                        print(','.join(str(v) for v in row))
            else:
                print("No results returned")
        else:
            print(f"ERROR: {result['error']}")

if __name__ == "__main__":
    main()
