#!/bin/bash
# Quick start script for Docker Compose on Linux/Mac

echo "🐳 Proiect Backend - Docker Quick Start"
echo "========================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker Desktop."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose."
    exit 1
fi

echo "✓ Docker found"
echo ""

# Ask user what they want to do
echo "What would you like to do?"
echo "1) Start containers (docker-compose up)"
echo "2) Stop containers (docker-compose down)"
echo "3) View logs"
echo "4) Access database shell"
echo "5) Full rebuild"
echo "6) Clean everything (remove volumes)"
echo ""
read -p "Choose option (1-6): " option

case $option in
    1)
        echo "🚀 Starting containers..."
        docker-compose up -d
        echo "✓ Containers started!"
        echo ""
        echo "API available at: http://localhost:8000"
        echo "API docs at: http://localhost:8000/docs"
        echo ""
        echo "View logs with: docker-compose logs -f"
        ;;
    2)
        echo "🛑 Stopping containers..."
        docker-compose down
        echo "✓ Containers stopped!"
        ;;
    3)
        echo "📋 Showing logs (press Ctrl+C to exit)..."
        docker-compose logs -f
        ;;
    4)
        echo "🗄️  Connecting to database..."
        docker-compose exec db psql -U proiect_user -d proiect_db
        ;;
    5)
        echo "🔨 Full rebuild..."
        docker-compose down -v
        docker-compose build --no-cache
        docker-compose up -d
        echo "✓ Rebuild complete!"
        echo ""
        echo "API available at: http://localhost:8000"
        ;;
    6)
        echo "🧹 Cleaning up everything..."
        docker-compose down -v
        docker image prune -a --force
        docker volume prune --force
        echo "✓ Cleanup complete!"
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac
