# etl_script.py
"""Example ETL script using dbcreds."""

import pandas as pd
from dbcreds import get_engine
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_sales_data(days_back=7):
    """Extract sales data from production database."""
    logger.info(f"Extracting sales data for last {days_back} days")
    
    engine = get_engine("production")
    
    query = """
        SELECT 
            order_id,
            customer_id,
            order_date,
            total_amount,
            status
        FROM orders
        WHERE order_date >= %(start_date)s
        AND status = 'completed'
    """
    
    start_date = datetime.now() - timedelta(days=days_back)
    
    df = pd.read_sql(
        query,
        engine,
        params={'start_date': start_date}
    )
    
    logger.info(f"Extracted {len(df)} orders")
    return df

def transform_sales_data(df):
    """Transform sales data for analytics."""
    logger.info("Transforming sales data")
    
    # Add calculated fields
    df['order_month'] = df['order_date'].dt.to_period('M')
    df['order_day_of_week'] = df['order_date'].dt.day_name()
    
    # Aggregate by customer
    customer_summary = df.groupby('customer_id').agg({
        'order_id': 'count',
        'total_amount': ['sum', 'mean'],
        'order_date': ['min', 'max']
    }).round(2)
    
    customer_summary.columns = [
        'order_count',
        'total_revenue',
        'avg_order_value',
        'first_order_date',
        'last_order_date'
    ]
    
    return customer_summary

def load_to_analytics(df):
    """Load transformed data to analytics database."""
    logger.info("Loading data to analytics database")
    
    engine = get_engine("analytics")
    
    df.to_sql(
        'customer_summary',
        engine,
        if_exists='replace',
        index=True,
        index_label='customer_id'
    )
    
    logger.info(f"Loaded {len(df)} customer records")

def main():
    """Run the ETL pipeline."""
    try:
        # Extract
        sales_df = extract_sales_data(days_back=30)
        
        # Transform
        customer_summary = transform_sales_data(sales_df)
        
        # Load
        load_to_analytics(customer_summary)
        
        logger.info("ETL pipeline completed successfully")
        
    except Exception as e:
        logger.error(f"ETL pipeline failed: {e}")
        raise

if __name__ == "__main__":
    main()
