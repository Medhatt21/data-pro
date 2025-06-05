#!/bin/bash

echo "🛑 Stopping Data Pro Stack..."
echo "============================="

# Stop all services
docker-compose down

echo ""
echo "✅ All services stopped successfully!"
echo ""
echo "💡 To remove all data volumes as well, run:"
echo "   docker-compose down -v"
echo ""
echo "🔄 To restart the stack, run:"
echo "   ./start.sh" 