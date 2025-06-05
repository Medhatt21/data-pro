import marimo

__generated_with = "0.9.14"
app = marimo.App(width="medium")


@app.cell
def __():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import psycopg2
    import redis
    from sqlalchemy import create_engine
    import os
    return np, os, pd, plt, psycopg2, redis, create_engine, sns


@app.cell
def __(os, create_engine):
    # Database connection setup
    postgres_host = os.getenv('POSTGRES_HOST', 'localhost')
    postgres_port = os.getenv('POSTGRES_PORT', '5432')
    postgres_db = os.getenv('POSTGRES_DB', 'data_pro')
    postgres_user = os.getenv('POSTGRES_USER', 'admin')
    postgres_password = os.getenv('POSTGRES_PASSWORD', 'admin123')
    
    # Create SQLAlchemy engine
    db_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
    engine = create_engine(db_url)
    
    print(f"Database connection configured for: {postgres_host}:{postgres_port}/{postgres_db}")
    return db_url, engine, postgres_db, postgres_host, postgres_password, postgres_port, postgres_user


@app.cell
def __(os, redis):
    # Redis connection setup
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    redis_password = os.getenv('REDIS_PASSWORD', 'redis123')
    
    try:
        r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
        r.ping()
        print(f"Redis connection successful: {redis_host}:{redis_port}")
    except Exception as e:
        print(f"Redis connection failed: {e}")
        r = None
    
    return r, redis_host, redis_password, redis_port


@app.cell
def __(np, pd):
    # Sample data creation
    sample_data = pd.DataFrame({
        'id': range(1, 101),
        'name': [f'Item_{i}' for i in range(1, 101)],
        'value': np.random.randn(100),
        'category': np.random.choice(['A', 'B', 'C'], 100),
        'timestamp': pd.date_range('2024-01-01', periods=100, freq='D')
    })
    
    print("Sample data created:")
    print(sample_data.head())
    return sample_data,


@app.cell
def __(engine, sample_data):
    # Save sample data to PostgreSQL
    try:
        sample_data.to_sql('sample_table', engine, if_exists='replace', index=False)
        print("Sample data saved to PostgreSQL successfully!")
    except Exception as e:
        print(f"Error saving to PostgreSQL: {e}")
    return


@app.cell
def __(engine, pd):
    # Read data from PostgreSQL
    try:
        df_from_db = pd.read_sql('SELECT * FROM sample_table LIMIT 10', engine)
        print("Data retrieved from PostgreSQL:")
        print(df_from_db)
    except Exception as e:
        print(f"Error reading from PostgreSQL: {e}")
        df_from_db = None
    return df_from_db,


@app.cell
def __(plt, sample_data, sns):
    # Data visualization
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # Histogram
    axes[0, 0].hist(sample_data['value'], bins=20, alpha=0.7)
    axes[0, 0].set_title('Value Distribution')
    
    # Box plot by category
    sns.boxplot(data=sample_data, x='category', y='value', ax=axes[0, 1])
    axes[0, 1].set_title('Value by Category')
    
    # Time series
    axes[1, 0].plot(sample_data['timestamp'], sample_data['value'])
    axes[1, 0].set_title('Value Over Time')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # Scatter plot
    axes[1, 1].scatter(sample_data['id'], sample_data['value'], alpha=0.6)
    axes[1, 1].set_title('Value vs ID')
    
    plt.tight_layout()
    plt.show()
    return axes, fig


@app.cell
def __(r):
    # Redis operations example
    if r:
        try:
            # Set some sample data in Redis
            r.set('sample_key', 'Hello from Marimo!')
            r.hset('sample_hash', mapping={'field1': 'value1', 'field2': 'value2'})
            
            # Retrieve data
            value = r.get('sample_key')
            hash_data = r.hgetall('sample_hash')
            
            print(f"Redis string value: {value}")
            print(f"Redis hash data: {hash_data}")
        except Exception as e:
            print(f"Redis operation error: {e}")
    return hash_data, value


if __name__ == "__main__":
    app.run() 