.PHONY: init up down logs status clean help

# Default target
help:
	@echo "Data Pro Stack - Available commands:"
	@echo "  make init   - Initialize the environment (copy .env, check Docker)"
	@echo "  make up     - Start the entire stack"
	@echo "  make down   - Stop the entire stack"
	@echo "  make logs   - View logs from all services"
	@echo "  make status - Show status of all services"
	@echo "  make clean  - Stop and remove all containers and volumes"
	@echo "  make help   - Show this help message"

# Initialize environment
init:
	@echo "🔧 Initializing Data Pro Stack..."
	@if [ ! -f .env ]; then \
		echo "📝 Creating .env file from template..."; \
		cp env.example .env; \
		echo "✅ .env file created. Please review and modify if needed."; \
	else \
		echo "✅ .env file already exists."; \
	fi
	@if ! docker info > /dev/null 2>&1; then \
		echo "❌ Docker is not running. Please start Docker first."; \
		exit 1; \
	else \
		echo "✅ Docker is running."; \
	fi
	@echo "🎉 Initialization complete!"

# Start the stack
up:
	@echo "🚀 Starting Data Pro Stack..."
	@./start.sh

# Stop the stack
down:
	@echo "🛑 Stopping Data Pro Stack..."
	@./stop.sh

# View logs
logs:
	@echo "📋 Viewing logs from all services..."
	@docker-compose logs -f

# Show status
status:
	@echo "📊 Service Status:"
	@echo "=================="
	@docker-compose ps

# Clean everything (stop and remove volumes)
clean:
	@echo "🧹 Cleaning up everything..."
	@echo "⚠️  This will remove all data volumes!"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	@docker-compose down -v
	@echo "✅ All containers and volumes removed!" 