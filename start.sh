#!/bin/bash

echo "🚀 Starting Data Pro Stack..."
echo "================================"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please run 'make init' first."
    exit 1
fi

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service status
echo "📊 Service Status:"
echo "=================="
docker-compose ps

echo ""
echo "🎉 Data Pro Stack is ready!"
echo "=========================="
echo ""
echo "📱 Access your services:"
echo "• n8n (Workflow Automation): http://localhost:5678"
echo "  └── Login: admin / admin123"
echo ""
echo "• Marimo (Python Notebooks): http://localhost:8888"
echo "  └── No login required"
echo ""
echo "• Superset (BI & Visualization): http://localhost:8088"
echo "  └── Login: admin / admin123"
echo ""
echo "• PostgreSQL Database: localhost:5432"
echo "  └── User: admin / Password: admin123"
echo ""
echo "• Redis Cache: localhost:6379"
echo "  └── Password: redis123"
echo ""
echo "📚 Check README.md for detailed usage instructions"
echo ""
echo "🛠️  Useful commands:"
echo "• View logs: docker-compose logs -f [service-name]"
echo "• Stop stack: docker-compose down"
echo "• Restart service: docker-compose restart [service-name]" 