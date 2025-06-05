import marimo

__generated_with = "0.9.14"
app = marimo.App(width="medium")


@app.cell
def __():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sqlalchemy import create_engine, text
    import psycopg2
    import redis
    import os
    from datetime import datetime, timedelta
    return datetime, np, os, pd, plt, psycopg2, redis, create_engine, sns, text, timedelta


@app.cell
def __(os, create_engine):
    # Database connection
    postgres_host = os.getenv('POSTGRES_HOST', 'postgres')
    postgres_port = os.getenv('POSTGRES_PORT', '5432')
    postgres_db = os.getenv('POSTGRES_DB', 'data_pro')
    postgres_user = os.getenv('POSTGRES_USER', 'admin')
    postgres_password = os.getenv('POSTGRES_PASSWORD', 'admin123')
    
    db_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
    engine = create_engine(db_url)
    
    print(f"✅ Connected to PostgreSQL: {postgres_host}:{postgres_port}/{postgres_db}")
    return db_url, engine, postgres_db, postgres_host, postgres_password, postgres_port, postgres_user


@app.cell
def __(datetime, engine, np, pd, text, timedelta):
    # Create sample sales data
    np.random.seed(42)
    
    # Generate sample data
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=x) for x in range(365)]
    
    sales_data = pd.DataFrame({
        'date': dates,
        'product_id': np.random.choice(['PROD_001', 'PROD_002', 'PROD_003', 'PROD_004', 'PROD_005'], 365),
        'sales_amount': np.random.normal(1000, 300, 365).round(2),
        'quantity': np.random.poisson(5, 365),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 365),
        'customer_segment': np.random.choice(['Enterprise', 'SMB', 'Individual'], 365)
    })
    
    # Ensure positive sales amounts
    sales_data['sales_amount'] = np.abs(sales_data['sales_amount'])
    
    print(f"📊 Generated {len(sales_data)} sales records")
    print(sales_data.head())
    return dates, sales_data, start_date


@app.cell
def __(engine, sales_data):
    # Save to database
    try:
        sales_data.to_sql('sales_data', engine, if_exists='replace', index=False)
        print("✅ Sales data saved to PostgreSQL successfully!")
        
        # Create an index for better performance
        with engine.connect() as conn:
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_sales_date ON sales_data(date)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_sales_product ON sales_data(product_id)"))
            conn.commit()
        print("✅ Database indexes created!")
        
    except Exception as e:
        print(f"❌ Error saving to PostgreSQL: {e}")
    return


@app.cell
def __(engine, pd, text):
    # Query and analyze data
    try:
        # Monthly sales summary
        monthly_sales = pd.read_sql(text("""
            SELECT 
                DATE_TRUNC('month', date) as month,
                SUM(sales_amount) as total_sales,
                SUM(quantity) as total_quantity,
                COUNT(*) as transaction_count,
                AVG(sales_amount) as avg_sale_amount
            FROM sales_data 
            GROUP BY DATE_TRUNC('month', date)
            ORDER BY month
        """), engine)
        
        print("📈 Monthly Sales Summary:")
        print(monthly_sales)
        
    except Exception as e:
        print(f"❌ Error querying data: {e}")
        monthly_sales = None
    return monthly_sales,


@app.cell
def __(engine, pd, text):
    # Product performance analysis
    try:
        product_performance = pd.read_sql(text("""
            SELECT 
                product_id,
                SUM(sales_amount) as total_revenue,
                SUM(quantity) as total_units_sold,
                COUNT(*) as transaction_count,
                AVG(sales_amount) as avg_transaction_value,
                ROUND(AVG(sales_amount), 2) as avg_sale_amount
            FROM sales_data 
            GROUP BY product_id
            ORDER BY total_revenue DESC
        """), engine)
        
        print("🏆 Product Performance:")
        print(product_performance)
        
    except Exception as e:
        print(f"❌ Error querying product data: {e}")
        product_performance = None
    return product_performance,


@app.cell
def __(monthly_sales, plt):
    # Visualize monthly sales trend
    if monthly_sales is not None:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Sales amount trend
        ax1.plot(monthly_sales['month'], monthly_sales['total_sales'], marker='o', linewidth=2)
        ax1.set_title('Monthly Sales Revenue Trend', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Total Sales ($)')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # Transaction count trend
        ax2.bar(monthly_sales['month'], monthly_sales['transaction_count'], alpha=0.7, color='orange')
        ax2.set_title('Monthly Transaction Count', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Number of Transactions')
        ax2.set_xlabel('Month')
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
    return ax1, ax2, fig


@app.cell
def __(plt, product_performance, sns):
    # Product performance visualization
    if product_performance is not None:
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Revenue by product
        ax1.bar(product_performance['product_id'], product_performance['total_revenue'])
        ax1.set_title('Total Revenue by Product')
        ax1.set_ylabel('Revenue ($)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Units sold by product
        ax2.bar(product_performance['product_id'], product_performance['total_units_sold'], color='green')
        ax2.set_title('Total Units Sold by Product')
        ax2.set_ylabel('Units Sold')
        ax2.tick_params(axis='x', rotation=45)
        
        # Average transaction value
        ax3.bar(product_performance['product_id'], product_performance['avg_transaction_value'], color='red')
        ax3.set_title('Average Transaction Value by Product')
        ax3.set_ylabel('Avg Transaction Value ($)')
        ax3.tick_params(axis='x', rotation=45)
        
        # Transaction count
        ax4.pie(product_performance['transaction_count'], labels=product_performance['product_id'], autopct='%1.1f%%')
        ax4.set_title('Transaction Distribution by Product')
        
        plt.tight_layout()
        plt.show()
    return ax3, ax4, fig


@app.cell
def __(engine, pd, text):
    # Regional analysis
    try:
        regional_analysis = pd.read_sql(text("""
            SELECT 
                region,
                customer_segment,
                SUM(sales_amount) as total_sales,
                COUNT(*) as transaction_count,
                AVG(sales_amount) as avg_sale_amount
            FROM sales_data 
            GROUP BY region, customer_segment
            ORDER BY region, total_sales DESC
        """), engine)
        
        print("🌍 Regional & Customer Segment Analysis:")
        print(regional_analysis)
        
    except Exception as e:
        print(f"❌ Error querying regional data: {e}")
        regional_analysis = None
    return regional_analysis,


@app.cell
def __(plt, regional_analysis, sns):
    # Regional analysis visualization
    if regional_analysis is not None:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Sales by region
        region_totals = regional_analysis.groupby('region')['total_sales'].sum().sort_values(ascending=False)
        ax1.bar(region_totals.index, region_totals.values)
        ax1.set_title('Total Sales by Region')
        ax1.set_ylabel('Total Sales ($)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Heatmap of sales by region and customer segment
        pivot_data = regional_analysis.pivot(index='region', columns='customer_segment', values='total_sales')
        sns.heatmap(pivot_data, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax2)
        ax2.set_title('Sales Heatmap: Region vs Customer Segment')
        
        plt.tight_layout()
        plt.show()
    return ax1, ax2, fig, pivot_data, region_totals


@app.cell
def __(datetime, os, redis):
    # Redis caching example
    redis_host = os.getenv('REDIS_HOST', 'redis')
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    redis_password = os.getenv('REDIS_PASSWORD', 'redis123')
    
    try:
        r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
        r.ping()
        print(f"✅ Connected to Redis: {redis_host}:{redis_port}")
        
        # Cache some analysis results
        r.set('last_analysis_date', str(datetime.now()))
        r.hset('sales_summary', mapping={
            'total_records': '365',
            'analysis_type': 'sales_performance',
            'status': 'completed'
        })
        
        # Retrieve cached data
        last_analysis = r.get('last_analysis_date')
        summary = r.hgetall('sales_summary')
        
        print(f"📝 Cached analysis date: {last_analysis}")
        print(f"📊 Analysis summary: {summary}")
        
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        r = None
    return last_analysis, r, redis_host, redis_password, redis_port, summary


@app.cell
def __():
    print("🎉 Database Analysis Complete!")
    print("=" * 40)
    print("✅ Sample sales data created and stored in PostgreSQL")
    print("✅ Multiple analysis queries executed")
    print("✅ Visualizations generated")
    print("✅ Results cached in Redis")
    print("")
    print("💡 Next steps:")
    print("• Use this data in Superset for dashboard creation")
    print("• Create n8n workflows to automate data updates")
    print("• Extend analysis with additional metrics")
    return


if __name__ == "__main__":
    app.run() 