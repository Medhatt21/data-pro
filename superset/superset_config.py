import os
from celery import Celery

# Database configuration
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

# Redis configuration
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

# Cache configuration
CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_HOST': REDIS_HOST,
    'CACHE_REDIS_PORT': REDIS_PORT,
    'CACHE_REDIS_PASSWORD': REDIS_PASSWORD,
    'CACHE_REDIS_DB': 1,
}

# Results backend for async queries
RESULTS_BACKEND = {
    'cache_type': 'RedisCache',
    'cache_default_timeout': 86400,  # 1 day
    'cache_config': {
        'host': REDIS_HOST,
        'port': REDIS_PORT,
        'password': REDIS_PASSWORD,
        'db': 2,
    }
}

# Celery configuration for async queries
class CeleryConfig:
    broker_url = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/3'
    result_backend = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/4'
    worker_prefetch_multiplier = 1
    task_acks_late = True
    task_annotations = {
        'sql_lab.get_sql_results': {
            'rate_limit': '100/s',
        },
    }

CELERY_CONFIG = CeleryConfig

# Security configuration
SECRET_KEY = os.getenv('SUPERSET_SECRET_KEY')

# Feature flags
FEATURE_FLAGS = {
    'ENABLE_TEMPLATE_PROCESSING': True,
    'DASHBOARD_NATIVE_FILTERS': True,
    'DASHBOARD_CROSS_FILTERS': True,
    'DASHBOARD_RBAC': True,
    'ENABLE_ADVANCED_DATA_TYPES': True,
}

# SQL Lab configuration
SQLLAB_CTAS_NO_LIMIT = True
SQLLAB_TIMEOUT = 300
SQLLAB_ASYNC_TIME_LIMIT_SEC = 600

# Email configuration (optional)
SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_STARTTLS = True
SMTP_SSL = False
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SMTP_MAIL_FROM = os.getenv('SMTP_MAIL_FROM')

# Webserver configuration
WEBSERVER_THREADS = 8
WEBSERVER_TIMEOUT = 60

# Enable CORS for development
ENABLE_CORS = True
CORS_OPTIONS = {
    'supports_credentials': True,
    'allow_headers': ['*'],
    'resources': ['*'],
    'origins': ['*']
}

# Row limit for SQL Lab
ROW_LIMIT = 5000
VIZ_ROW_LIMIT = 10000

# CSV export encoding
CSV_EXPORT = {
    'encoding': 'utf-8',
}

# Enable public role
PUBLIC_ROLE_LIKE = 'Gamma'

# Custom CSS
CUSTOM_CSS = """
.navbar-brand {
    font-weight: bold;
}
""" 