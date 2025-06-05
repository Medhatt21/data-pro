# Data Pro Stack

A comprehensive Docker-based stack for data engineering automation, data analytics, and AI/data science project hosting.

With built-in tools like n8n, Marimo, PostgreSQL, Superset, and Redis, this stack enables you to:

Automate data workflows (e.g., scrape APIs daily, clean and store results)

Perform analytics and create dashboards (e.g., real-time sales monitoring, A/B test analysis)

Host and run data science projects and AI apps (e.g., deploy ML notebooks, analyze customer insights, build RAG chatbots)

- **n8n**: Workflow automation platform
- **Marimo**: Interactive Python notebooks
- **PostgreSQL**: Primary database
- **Apache Superset**: Business intelligence and data visualization
- **Redis**: Caching and message broker

## Quick Start


> **Requirements**:  
> - [Docker](https://docs.docker.com/get-docker/) must be installed and running  
> - [`make`](https://www.gnu.org/software/make/) is required  
>   - Available by default on Linux/macOS  
>   - For Windows, use WSL or install via [GnuWin](http://gnuwin32.sourceforge.net/packages/make.htm)

1. **Clone and setup**:
   ```bash
   git clone https://github.com/Medhatt21/data-pro.git
   cd data-pro
   ```

2. **Initialize and start**:
   ```bash
   make init    # Initialize environment
   make up      # Start the stack
   ```

3. **Access the services**:
   - **n8n**: http://localhost:5678 (admin/admin123)
   - **Marimo**: http://localhost:8888
   - **Superset**: http://localhost:8088 (admin/admin123)
   - **PostgreSQL**: localhost:5432 (admin/admin123)
   - **Redis**: localhost:6379 (password: redis123)

## Services Overview

### n8n (Workflow Automation)
- **URL**: http://localhost:5678
- **Credentials**: admin/admin123
- **Database**: PostgreSQL (n8n database)
- **Features**: 
  - Visual workflow builder
  - 200+ integrations
  - Webhook support
  - Scheduled workflows

### Marimo (Interactive Notebooks)
- **URL**: http://localhost:8888
- **Features**:
  - Reactive Python notebooks (Python 3.13 + uv package manager)
  - Pre-configured with data science libraries
  - Database connectivity (PostgreSQL + Redis)
  - Sample notebooks in lab_root directory

### Apache Superset (BI & Visualization)
- **URL**: http://localhost:8088
- **Credentials**: admin/admin123
- **Database**: PostgreSQL (superset database)
- **Cache**: Redis
- **Features**:
  - Rich visualizations
  - SQL Lab
  - Dashboard builder
  - Role-based access control

### PostgreSQL (Database)
- **Host**: localhost:5432
- **Credentials**: admin/admin123
- **Databases**:
  - `data_pro` (main database)
  - `n8n` (n8n workflows)
  - `superset` (superset metadata)

### Redis (Cache & Message Broker)
- **Host**: localhost:6379
- **Password**: redis123
- **Usage**:
  - Superset caching
  - Session storage
  - Message queuing

## Directory Structure

```
data-pro/
├── Makefile                    # Easy management commands
├── docker-compose.yml          # Main orchestration file
├── env.example                 # Environment variables template
├── start.sh / stop.sh         # Stack management scripts
├── lab_root/                   # Marimo notebooks workspace
│   ├── sample_notebook.py     # Basic connectivity example
│   └── database_example.py    # Advanced analysis example
├── postgres/
│   └── init-multiple-databases.sh  # DB initialization script
├── marimo/
│   ├── Dockerfile             # Marimo container (Python 3.13 + uv)
│   └── pyproject.toml         # Python dependencies
└── superset/
    ├── Dockerfile             # Superset container (official image)
    ├── superset_config.py     # Superset configuration
    └── init_superset.sh       # Superset initialization
```

## Data Flow & Integration

1. **Data Ingestion**: Use n8n to create workflows that fetch data from various sources
2. **Data Storage**: Store processed data in PostgreSQL
3. **Data Analysis**: Use Marimo notebooks for exploratory data analysis
4. **Data Visualization**: Create dashboards and reports in Superset
5. **Caching**: Redis provides fast access to frequently used data

## Development Workflow

### Adding Data Sources to Superset

1. Access Superset at http://localhost:8088
2. Go to **Data** → **Databases**
3. Add your PostgreSQL connection:
   - **Database**: `postgresql://admin:admin123@postgres:5432/data_pro`
   - **Display Name**: `Main Database`

### Creating Workflows in n8n

1. Access n8n at http://localhost:5678
2. Create new workflow
3. Use database nodes to connect to PostgreSQL
4. Use HTTP Request nodes for external APIs
5. Use Redis nodes for caching

### Using Marimo Notebooks

1. Access Marimo at http://localhost:8888
2. Open the sample notebooks to see database connectivity examples
3. Create new notebooks for your analysis
4. All notebooks are persisted in the `lab_root` directory

## Configuration

### Environment Variables

Copy `env.example` to `.env` and modify as needed:

- **Database credentials**: Change default passwords
- **Redis password**: Update for security
- **Superset secret key**: Generate a secure key for production

### Persistent Data

All data is persisted using Docker volumes:
- `postgres_data`: Database files
- `redis_data`: Redis persistence
- `n8n_data`: n8n workflows and settings
- `marimo_data`: Notebook files (mounted to lab_root)
- `superset_data`: Superset configuration and metadata

**Configuration is centralized** through environment variables in the `.env` file.

## Production Considerations

1. **Security**:
   - Change all default passwords
   - Use environment-specific secrets
   - Enable SSL/TLS for external access
   - Configure proper firewall rules

2. **Performance**:
   - Adjust PostgreSQL configuration for your workload
   - Configure Redis memory limits
   - Scale services horizontally if needed

3. **Backup**:
   - Regular PostgreSQL backups
   - Export n8n workflows
   - Backup Superset dashboards

## Troubleshooting

### Service Won't Start
```bash
# Check service logs
make logs
# or for specific service:
docker-compose logs <service-name>

# Check service status
make status

# Restart specific service
docker-compose restart <service-name>
```

### Database Connection Issues
```bash
# Check PostgreSQL logs
docker-compose logs postgres

# Test connection
docker-compose exec postgres psql -U admin -d data_pro
```

### Reset Everything
```bash
# Stop and remove all containers and volumes
make clean
make up
```

## Make Commands

The project includes a Makefile for easy management:

```bash
make init     # Initialize environment (.env file, check Docker)
make up       # Start the entire stack
make down     # Stop the stack
make logs     # View logs from all services
make status   # Show status of all services
make clean    # Stop and remove all containers and volumes
make help     # Show available commands
```

## Support

For issues and questions:
1. Check service logs: `make logs` or `docker-compose logs <service>`
2. Check service status: `make status`
3. Verify network connectivity between services
4. Ensure all environment variables are properly set
5. Check that all required ports are available 